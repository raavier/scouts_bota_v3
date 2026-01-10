import pandas as pd

# Carregar arquivo consolidado
df = pd.read_parquet('bases/outputs/consolidated_overral.parquet')

# Lista de alguns player_ids da imagem
sample_players = [523978, 520106, 445998, 419029, 196875, 410697, 406907]

print("="*80)
print("ANÁLISE DE JOGADORES COM VALORES ZERADOS")
print("="*80)

# Verificar jogadores da amostra
print("\nJogadores da amostra:")
for player_id in sample_players:
    player = df[df['player_id'] == player_id]
    if len(player) > 0:
        p = player.iloc[0]
        print(f"\nPlayer ID: {player_id}")
        print(f"  Nome: {p['player_name']}")
        print(f"  Posição: {p['mapped_position']}")
        print(f"  Overall Score: {p['overall_score']}")

        # Verificar se tem valores zerados nas colunas de score
        score_cols = [c for c in df.columns if 'score_' in c]
        scores = player[score_cols].iloc[0]
        zero_scores = scores[scores == 0]
        print(f"  Scores zerados: {len(zero_scores)}/{len(scores)}")

# Estatísticas gerais
print("\n" + "="*80)
print("ESTATÍSTICAS GERAIS")
print("="*80)

print(f"\nTotal de jogadores: {len(df)}")
print(f"Jogadores com overall_score = 0: {(df['overall_score'] == 0).sum()}")
print(f"Jogadores com overall_score > 0: {(df['overall_score'] > 0).sum()}")

# Verificar se há algum padrão
zeros = df[df['overall_score'] == 0]
if len(zeros) > 0:
    print(f"\n{len(zeros)} jogadores com overall_score = 0")
    print("\nDistribuição por posição:")
    print(zeros['mapped_position'].value_counts())

    print("\nDistribuição por competição:")
    print(zeros['competition_name'].value_counts())

    # Verificar se esses jogadores têm dados de indicadores
    print("\n" + "="*80)
    print("DIAGNÓSTICO: Verificando indicadores dos jogadores com score = 0")
    print("="*80)

    # Pegar um exemplo de jogador com score 0
    example = zeros.iloc[0]
    print(f"\nExemplo: {example['player_name']} (ID: {example['player_id']})")
    print(f"Posição: {example['mapped_position']}")
    print(f"Time: {example['team_name']}")
    print(f"Competição: {example['competition_name']}")

    # Carregar dados normalizados para verificar
    df_norm = pd.read_parquet('bases/outputs/consolidated_normalized.parquet')
    player_norm = df_norm[df_norm['player_id'] == example['player_id']]

    if len(player_norm) > 0:
        # Verificar colunas normalizadas
        norm_cols = [c for c in player_norm.columns if c.endswith('_norm')]
        if norm_cols:
            norm_values = player_norm[norm_cols].iloc[0]
            non_zero = (norm_values > 0).sum()
            print(f"\nIndicadores normalizados:")
            print(f"  Total: {len(norm_values)}")
            print(f"  Não-zero: {non_zero}")
            print(f"  Zero: {len(norm_values) - non_zero}")

            if non_zero > 0:
                print(f"\nAlguns valores não-zero:")
                print(norm_values[norm_values > 0].head(10))
else:
    print("\nTodos os jogadores têm overall_score > 0")
