import pandas as pd
from unidecode import unidecode

df = pd.read_csv("mercadolibre.csv")

print(df.shape)
print(df.columns)
df.head()

results_ = []
for i in range(df.shape[0]):
    try:
        features_list = df["features"].iloc[i].split(",")
        values_list = df["values"].iloc[i].split(",")
        vars_i = dict(zip(features_list, values_list))
        results_.append(vars_i)
    except:
        print("error ix:", i, df["values"].iloc[i])
        results_.append({})

results_df = pd.DataFrame(results_)
assert results_df.shape[0] == df.shape[0]

results_df.columns = results_df.columns.str.lower()
results_df.columns = [unidecode(x).strip().replace(" ", "_") for x in results_df.columns]


nulls_ = results_df.isnull().mean()
nulls_ = nulls_.sort_values()
cols_drop = nulls_[nulls_>0.6].index
results_df = results_df.drop(columns=cols_drop)


results_df["area_total"] = results_df["area_total"].str.split(" ").str[0].str.strip().astype(float)
results_df["area_construida"] = results_df["area_construida"].str.split(" ").str[0].str.strip().astype(float)
results_df["habitaciones"] = results_df["habitaciones"].astype("Int64")
results_df["banos"] = results_df["banos"].astype("Int64")
results_df["estacionamientos"] = results_df["estacionamientos"].astype("Int64")
results_df["antiguedad"] = results_df["antiguedad"].str.split(" ").str[0].str.strip().astype(float)
results_df["administracion"] = results_df["administracion"].str.split(" ").str[0].str.strip().astype(float)
results_df["estrato_social"] = results_df["estrato_social"].astype("Int64")

cols_dummies = [
    'armarios',
    'lavanderia', 
    'gas_natural', 
    'area_de_juegos_infantiles',
    'seguridad',
    'balcon',
    'area_de_bbq',
    'estudio',
    'calefaccion'
]
for x in cols_dummies:
    results_df[x] = results_df[x].fillna("sin_dato")
    results_df[x] = results_df[x].str.lower().str.replace("í", "i")

results_df.head()
results_df.dtypes

df["precio"] = df["precio"].str.replace(".", "").astype(float)
df["lat"] = df["coords"].str.split(",").str[0]
df["long"] = df["coords"].str.split(",").str[1]

df = df.drop(columns=["features", "values", "coords", "titulo"])

df_total = df.join(results_df)
print(df.shape)
print(results_df.shape)
df_total.head()

df_total["precio_m2"] = df_total["precio"] / df_total["area_total"]
df_total["tipo_inmueble"] = df_total["tipo_inmueble"].str.split(" ").str[0]
df_total["tipo_inmueble"] = df_total["tipo_inmueble"].str.lower()

df_total["administracion"] = df_total["administracion"].fillna(0)
df_total = df_total[(df_total["estrato_social"] <= 6) | (df_total["estrato_social"].isnull())]
print(df_total.shape)
df_total = df_total[df_total["antiguedad"] >= 0]
df_total = df_total[df_total["antiguedad"] <= 100]
print(df_total.shape)


df_total.to_csv("mercadolibre_procesado.csv", index=False)