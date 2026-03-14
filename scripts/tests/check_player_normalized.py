import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Carregar o parquet
df = pd.read_parquet(BASE_DIR / "bases" / "outputs" / "consolidated_normalized.parquet")

# Filtrar pela unique_key
unique_key = "424480_81_1343"
player_data = df[df["unique_key"] == unique_key].copy()

print("=" * 100)
print(f"DADOS NORMALIZADOS PARA unique_key: {unique_key}")
print("=" * 100)

if len(player_data) == 0:
    print(f"\nNenhum dado encontrado para unique_key = '{unique_key}'")
else:
    print(f"\nTotal de registros encontrados: {len(player_data)}")
    print(f"Total de colunas: {len(player_data.columns)}")

    # Informações básicas
    print("\n" + "-" * 100)
    print("INFORMAÇÕES BÁSICAS:")
    print("-" * 100)
    basic_cols = ["unique_key", "player_id", "competition_id", "mapped_position", "v_current"]
    print(player_data[basic_cols].to_string(index=False))

    # Colunas normalizadas
    norm_cols = [c for c in player_data.columns if c.endswith("_norm")]
    print(f"\n" + "-" * 100)
    print(f"COLUNAS NORMALIZADAS: {len(norm_cols)} indicadores")
    print("-" * 100)

    # Transpor para mostrar melhor
    # Pegar apenas o registro v_current = True
    current_data = player_data[player_data["v_current"] == True]

    if len(current_data) > 0:
        print("\nValores normalizados (v_current = True):")
        print("-" * 100)
        for col in norm_cols:
            value = current_data[col].values[0]
            print(f"{col:50} = {value:>10.6f}")
    else:
        print("\nNenhum registro com v_current = True encontrado.")
        print("\nMostrando valores do primeiro registro:")
        print("-" * 100)
        for col in norm_cols:
            value = player_data[col].iloc[0]
            print(f"{col:50} = {value:>10.6f}")

    # Se houver múltiplos registros, mostrar comparação
    if len(player_data) > 1:
        print(f"\n" + "=" * 100)
        print(f"COMPARAÇÃO ENTRE OS {len(player_data)} REGISTROS (Primeiros 10 indicadores):")
        print("=" * 100)

        # Criar dataframe transposto com os primeiros 10 indicadores
        sample_cols = norm_cols[:10]
        comparison = player_data[["v_current"] + sample_cols].copy()
        comparison["periodo"] = range(1, len(comparison) + 1)

        for col in sample_cols:
            print(f"\n{col}:")
            for _, row in comparison.iterrows():
                current_marker = " <-- ATUAL" if row["v_current"] else ""
                print(f"  Período {row['periodo']}: {row[col]:>10.6f}{current_marker}")

print("\n" + "=" * 100)
