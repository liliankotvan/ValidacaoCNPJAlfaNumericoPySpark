from pyspark.sql.functions import col, upper, regexp_replace
from pyspark.sql.types import StructType, StructField, BooleanType, StringType
from pyspark.sql.utils import AnalysisException

# Mapeamento ASCII - 48
ascii_map = {str(i): i for i in range(10)}
ascii_map.update({chr(i): i - 48 for i in range(65, 91)})

# Função local que valida o CNPJ alfanumérico
def validar_cnpj(cnpj):
    def ascii_val(c): return ascii_map.get(c.upper(), 0)
    if len(cnpj) != 14: return False, "Tamanho incorreto"
    
    base = cnpj[:12]
    dv_real = cnpj[12:]

    pesos_1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    soma1 = sum(ascii_val(c)*p for c,p in zip(base, pesos_1))
    dv1 = 0 if soma1 % 11 < 2 else 11 - (soma1 % 11)

    base_13 = base + str(dv1)
    pesos_2 = [6] + pesos_1
    soma2 = sum(ascii_val(c)*p for c,p in zip(base_13, pesos_2))
    dv2 = 0 if soma2 % 11 < 2 else 11 - (soma2 % 11)

    dv_calc = f"{dv1}{dv2}"
    if dv_calc == dv_real:
        return True, "Válido"
    elif dv_real[0] != str(dv1) and dv_real[1] != str(dv2):
        return False, "Ambos inválidos"
    elif dv_real[0] != str(dv1):
        return False, "DV1 inválido"
    else:
        return False, "DV2 inválido"

# Função principal: recebe nome da tabela, da coluna e opcionalmente da tabela de log
def executar_validacao(spark, tabela_origem, coluna_cnpj, tabela_log=None):
    from pyspark.sql.functions import udf
    schema = StructType([
        StructField("valido", BooleanType(), True),
        StructField("diagnostico", StringType(), True)
    ])
    udf_valida = udf(validar_cnpj, schema)

    df = spark.table(tabela_origem)
    df = df.withColumn("cnpj_formatado", upper(regexp_replace(col(coluna_cnpj), r"[^A-Z0-9]", "")))
    df = df.withColumn("resultado", udf_valida(col("cnpj_formatado")))
    df_final = df.select("*", col("resultado.valido").alias("valido"), col("resultado.diagnostico").alias("diagnostico"))

    if tabela_log:
        df_invalidos = df_final.filter(~col("valido"))
        try:
            spark.sql(f"DESCRIBE TABLE {tabela_log}")
            cols = [f.name.lower() for f in spark.table(tabela_log).schema.fields]
            if "cnpj" not in cols or "valido" not in cols:
                return f"⚠️ Tabela '{tabela_log}' existe, mas precisa conter colunas 'cnpj' e 'valido'."

            df_log = df_invalidos.select(col(coluna_cnpj).alias("cnpj"), col("valido"))
            df_log.createOrReplaceTempView("log_temp")

            spark.sql(f"""
                MERGE INTO {tabela_log} AS destino
                USING log_temp AS origem
                ON destino.cnpj = origem.cnpj
                WHEN MATCHED THEN UPDATE SET destino.valido = origem.valido
                WHEN NOT MATCHED THEN INSERT (cnpj, valido) VALUES (origem.cnpj, origem.valido)
            """)
        except AnalysisException:
            return f"⚠️ Tabela '{tabela_log}' não existe."
        except Exception as e:
            return f"⚠️ Erro ao gravar logs: {str(e)}"

    return "✅ Validação concluída com sucesso."
