import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


df = pd.read_csv("mercadolibre_procesado.csv")
df.head()
df.columns

cols_ = [
    "precio_m2",
    "tipo_inmueble",
    "habitaciones", 
    "banos",
    "estacionamientos",
    "antiguedad",
    "administracion",
    "estrato_social"
]
df = df[cols_]

print(df.isnull().mean())

train, test = train_test_split(
    df,
    test_size=0.1,
    stratify=df["tipo_inmueble"],
    random_state=421
)
print(train.shape)
print(test.shape)

## analisis de los datos de train
q_ = [0, 0.01, 0.02, 0.5, 0.9, 0.95, 0.98, 0.99, 1]
# train["precio_m2"].quantile(q_)
# train["habitaciones"].value_counts(dropna=False, normalize=True).sort_index().cumsum()
# train["banos"].value_counts(dropna=False, normalize=True).sort_index().cumsum()
# train["estacionamientos"].value_counts(dropna=False, normalize=True).sort_index().cumsum()
# train["antiguedad"].quantile(q_)
# train["administracion"].quantile(q_)
# train["estrato_social"].value_counts(dropna=False, normalize=True).sort_index().cumsum()

def preprocess_data(df: pd.DataFrame):

    data = df.copy()

    data = data.query("precio_m2 > 1000000")
    data = data.query("precio_m2 < 12000000")
    data["habitaciones"] = np.where(data["habitaciones"] >= 6, 6, data["habitaciones"])
    data["banos"] = np.where(data["banos"] >= 6, 6, data["banos"])
    data["estacionamientos"] = np.where(data["estacionamientos"] >= 4, 4, data["banos"])
    data["administracion"] = np.where(data["administracion"] >= 1000000, 1000000, data["banos"])

    return data


train_process = preprocess_data(train)
test_process = preprocess_data(test)

print(train.shape)
print(test.shape)


def prepare_data(
    df: pd.DataFrame,
    target_str: str,
    cols_drop: list
):    
    data = df.copy()
    data = data.drop(columns=cols_drop)
    print(f"Cantidad de registros: {data.shape}")

    if "tipo_inmueble" in data.columns:
        data["tipo_inmueble"] = (data["tipo_inmueble"] == "casa").astype(int)
    
    print(data.isnull().mean())
    data = data.dropna()
    print(f"Cantidad de registros despues de remover NAs: {data.shape}")

    return data.drop(columns=[target_str]), data[target_str]

cols_drop = [
    "administracion"
]
print("Train")
X_train, y_train = prepare_data(
    df=train,
    target_str="precio_m2",
    cols_drop=cols_drop
)
print("Test")
X_test, y_test = prepare_data(
    df=test,
    target_str="precio_m2",
    cols_drop=cols_drop
)
print(X_train.shape)
print(X_test.shape)

#for x in X_train.columns:
#    print(X_train.corr()[x])

### modelacion
from sklearn.linear_model import QuantileRegressor
from sklearn.utils.fixes import sp_version, parse_version

def fit_quantile_regression(X_train, y_train, X_test, y_test, quantile: float):
    # This is line is to avoid incompatibility if older SciPy version.
    # You should use `solver="highs"` with recent version of SciPy.
    solver = "highs" if sp_version >= parse_version("1.6.0") else "interior-point"

    qr = QuantileRegressor(quantile=quantile, alpha=0, solver=solver)
    qr = qr.fit(X_train, y_train)
    y_pred_train = qr.predict(X_train)
    y_pred_test = qr.predict(X_test)

    MDPE_train = np.median(np.abs(y_train - y_pred_train) / y_train) * 100
    MDPE_test = np.median(np.abs(y_test - y_pred_test) / y_test) * 100

    print(
        f"""Training Error
        MDPE={MDPE_train:.2f}%
    Test Error
        MDPE={MDPE_test:.2f}%
        """
    )
    features_names = ["intercept"] + list(qr.feature_names_in_)
    coef_values = [qr.intercept_] + list(qr.coef_)
    dict_coeficientes = dict(zip(features_names, coef_values))

    return qr, dict_coeficientes

qr, dict_coeficientes_sugerido = fit_quantile_regression(X_train, y_train, X_test, y_test, quantile=0.4)

qr_li, dict_coeficientes_li = fit_quantile_regression(X_train, y_train, X_test, y_test, quantile=0.3)

qr_ls, dict_coeficientes_ls = fit_quantile_regression(X_train, y_train, X_test, y_test, quantile=0.5)

print(dict_coeficientes_sugerido)
print(dict_coeficientes_li)
print(dict_coeficientes_ls)
