import os
import pandas as pd
import numpy as np
import sqlalchemy as sa

RAW_DIR = "data/raw/"
CLEAN_DIR = "data/clean/"

os.makedirs(CLEAN_DIR, exist_ok=True)

engine = sa.create_engine("sqlite:///agro.db")  
# For Postgres:
# engine = sa.create_engine("postgresql://user:pass@localhost/db")


# --------------------------------------------
# Helpers
# --------------------------------------------
def load_file(path):
    if path.endswith(".csv"):
        return pd.read_csv(path, encoding="utf-8")
    if path.endswith(".xlsx") or path.endswith(".xls"):
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file format: {path}")


def clean_columns(df):
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace(r"[^a-z0-9_]+", "", regex=True)
    )
    return df


def normalize_strings(df, cols):
    for col in cols:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df


def write_clean(df, name):
    path = os.path.join(CLEAN_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    return df


def to_sql(df, table):
    df.to_sql(table, engine, if_exists="replace", index=False)


# --------------------------------------------
# ETL per dataset
# --------------------------------------------

def etl_units_irrigation():
    df = load_file(RAW_DIR + "1_unidades_riego.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "municipio"])
    df["porcentaje_riego"] = df["porcentaje_riego"].astype(float)
    write_clean(df, "units_irrigation")
    to_sql(df, "units_irrigation")
    return df


def etl_production_open_field():
    df = load_file(RAW_DIR + "2_produccion_cielo_abierto.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "cultivo"])
    df["superficie_cultivada"] = df["superficie_cultivada"].fillna(0)
    df["produccion_ton"] = df["produccion_ton"].fillna(0)
    df["rendimiento"] = df["produccion_ton"] / df["superficie_cultivada"].replace({0: np.nan})
    write_clean(df, "production_open_field")
    to_sql(df, "production_open_field")
    return df


def etl_modalidad_hidrica():
    df = load_file(RAW_DIR + "3_modalidad_hidrica.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "cultivo"])
    df["superficie_cultivada"] = df["superficie_cultivada"].fillna(0)
    df["produccion"] = df["produccion"].fillna(0)
    df["rendimiento"] = df["produccion"] / df["superficie_cultivada"].replace({0: np.nan})
    write_clean(df, "modalidad_hidrica")
    to_sql(df, "modalidad_hidrica")
    return df


def etl_ciclo_oi():
    df = load_file(RAW_DIR + "4_ciclo_oi.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "cultivo"])
    df["rendimiento"] = df["produccion"] / df["superficie"].replace({0: np.nan})
    write_clean(df, "ciclo_oi")
    to_sql(df, "ciclo_oi")
    return df


def etl_ciclo_pv():
    df = load_file(RAW_DIR + "5_ciclo_pv.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "cultivo"])
    df["rendimiento"] = df["produccion"] / df["superficie"].replace({0: np.nan})
    write_clean(df, "ciclo_pv")
    to_sql(df, "ciclo_pv")
    return df


def etl_perennes():
    df = load_file(RAW_DIR + "6_perennes.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "cultivo"])
    df["superficie"] = df["superficie"].fillna(0)
    write_clean(df, "perennes")
    to_sql(df, "perennes")
    return df


def etl_land_use():
    df = load_file(RAW_DIR + "7_uso_suelo.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad"])
    write_clean(df, "land_use")
    to_sql(df, "land_use")
    return df


def etl_instalaciones():
    df = load_file(RAW_DIR + "8_instalaciones.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "municipio"])
    write_clean(df, "instalaciones")
    to_sql(df, "instalaciones")
    return df


def etl_uso_suelo_upa():
    df = load_file(RAW_DIR + "9_uso_suelo_upa.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "municipio"])
    write_clean(df, "uso_suelo_upa")
    to_sql(df, "uso_suelo_upa")
    return df


def etl_tecnologia():
    df = load_file(RAW_DIR + "10_tecnologia_agricola.csv")
    df = clean_columns(df)
    df = normalize_strings(df, ["entidad", "municipio"])
    df.rename(columns={"porcentaje": "porcentaje_uso"}, inplace=True)
    write_clean(df, "tecnologia")
    to_sql(df, "tecnologia")
    return df


# --------------------------------------------
# Master pipeline
# --------------------------------------------
def run_all():
    print("Running ETL...")
    etl_units_irrigation()
    etl_production_open_field()
    etl_modalidad_hidrica()
    etl_ciclo_oi()
    etl_ciclo_pv()
    etl_perennes()
    etl_land_use()
    etl_instalaciones()
    etl_uso_suelo_upa()
    etl_tecnologia()
    print("ETL Completed.")


if __name__ == "__main__":
    run_all()
