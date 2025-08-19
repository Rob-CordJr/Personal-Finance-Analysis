
import numpy as np
from sklearn.mixture import GaussianMixture



def segmentacao_risco_final(df):

    fatores_regionais = {
        'Europe': 1.05,
        'North America': 1.03,
        'Asia': 1.00,
        'Other': 0.98,
        'Africa': 0.95
    }

    fatores_emprego = {
        'Employed': 1.05,
        'Self-employed': 1.00,
        'Student': 0.95,
        'Unemployed': 0.90
    }


    df['score_ajustado'] = df.apply(lambda x: (
        x['credit_score'] *
        fatores_regionais.get(x['region'], 1.0) *
        fatores_emprego.get(x['employment_status'], 1.0) -
        (x['debt_to_income_ratio'] * 2)
    ), axis=1)


    limiar_baixo = df['score_ajustado'].quantile(0.75)
    limiar_alto = df['score_ajustado'].quantile(0.25)

    conditions = [
        (df['score_ajustado'] >= limiar_baixo) &
        (df['debt_to_income_ratio'] < 35) &
        (df['monthly_income_usd'] > 3000),

        (df['score_ajustado'] <= limiar_alto) |
        (df['debt_to_income_ratio'] > 45) |
        (df['employment_status'] == 'Unemployed')
    ]

    choices = ['Baixo Risco', 'Alto Risco']
    df['risco_final'] = np.select(conditions, choices, default='Médio Risco')

    return df


def segmentacao_risco_final_v2(df):

    gmm = GaussianMixture(n_components=2, random_state=42)
    scores = df['credit_score'].values.reshape(-1, 1)
    gmm.fit(scores)
    df['grupo_natural'] = gmm.predict(scores)


    fatores_regionais_v2 = {
        'Europe': 1.07,
        'North America': 1.04,
        'Asia': 1.00,
        'Other': 0.97,
        'Africa': 0.93
    }

    fatores_emprego_v2 = {
        'Employed': 1.07,
        'Self-employed': 1.02,
        'Student': 0.96,
        'Unemployed': 0.85
    }


    df['score_final'] = df.apply(lambda x: (
        x['credit_score'] *
        fatores_regionais_v2.get(x['region'], 1.0) *
        fatores_emprego_v2.get(x['employment_status'], 1.0) -
        (x['debt_to_income_ratio'] * 2.5) +
        (x['savings_to_income_ratio'] * 0.5)
    ), axis=1)


    limiares = {
        'Baixo Risco': df['score_final'].quantile(0.70),
        'Alto Risco': df['score_final'].quantile(0.30)
    }


    conditions = [
        (df['score_final'] >= limiares['Baixo Risco']) &
        (df['debt_to_income_ratio'] < 30) &
        (df['monthly_income_usd'] > 3000) &
        (df['employment_status'] != 'Unemployed'),

        (df['score_final'] <= limiares['Alto Risco']) |
        (df['debt_to_income_ratio'] > 45) |
        (df['employment_status'] == 'Unemployed') |
        (df['savings_to_income_ratio'] < 5)
    ]

    choices = ['Baixo Risco', 'Alto Risco']
    df['risco_final_v2'] = np.select(conditions, choices, default='Médio Risco')

    return df

def criar_grupos_estrategicos(df):

    mediana_renda = df['monthly_income_usd'].median()
    p75_income = df['monthly_income_usd'].quantile(0.75)
    p90_income = df['monthly_income_usd'].quantile(0.90)
    mediana_score = df['credit_score'].median()


    df['savings_ratio'] = df['savings_usd'] / (df['monthly_income_usd'].replace(0, 1))  # Evitar divisão por zero
    df['dti_ajustado'] = np.where(df['debt_to_income_ratio'] > 50, 50, df['debt_to_income_ratio'])


    has_job_tenure = 'job_tenure_months' in df.columns
    if not has_job_tenure:

        df['employment_stability'] = np.where(
            df['employment_status'] == 'Employed',
            df['age'] - 20,
            0
        )

    # Criar índice de estabilidade financeira adaptável
    stability_components = [
        0.4 * (df['credit_score']/850),
        0.3 * (1 - df['dti_ajustado']/50),
        0.2 * np.log1p(df['savings_usd'])/10
    ]

    if has_job_tenure:
        stability_components.append(0.1 * (df['job_tenure_months']/60))
    else:
        stability_components.append(0.1 * (df['employment_stability']/40))

    df['financial_stability_index'] = sum(stability_components)

    conditions = [

        (df['education_level'].isin(['PhD', 'Master'])) &
        (df['monthly_income_usd'] >= p90_income) &
        (df['credit_score'] >= mediana_score + 75) &
        (df['dti_ajustado'] < 15) &
        (df['savings_usd'] > df['monthly_income_usd'] * 18) &
        (df['financial_stability_index'] > 0.8),


        (df['education_level'].isin(['PhD', 'Master', 'Bachelor'])) &
        (df['monthly_income_usd'] >= p75_income * 1.1) &
        (df['credit_score'] >= mediana_score + 40) &
        (df['employment_status'] == 'Employed') &  # Mais conservador
        (df['dti_ajustado'] < 25) &
        (df['financial_stability_index'] > 0.7),


        (df['education_level'].isin(['PhD', 'Master'])) &
        (df['monthly_income_usd'] >= p75_income * 0.85) &
        (df['credit_score'] >= mediana_score + 20) &
        (df['age'] < 40) &  # Faixa etária ampliada
        (df['savings_ratio'] > 0.2) &  # Poupança mais robusta
        (df['employment_status'] != 'Unemployed') &
        (df['financial_stability_index'] > 0.65),


        (df['education_level'].isin(['PhD', 'Master'])) &
        (df['monthly_income_usd'] > mediana_renda * 1.3) &  # 30% acima da mediana
        (df['credit_score'] >= mediana_score) &
        (df['dti_ajustado'] < 35),

        (df['employment_status'] == 'Employed') &
        (df['credit_score'] > mediana_score + 20) &
        (df['dti_ajustado'] < 40),

        (df['employment_status'] == 'Employed'),

        (df['employment_status'].isin(['Self-employed', 'Student'])) &
        (df['monthly_income_usd'] > mediana_renda * 0.8) &  # Limiar elevado
        (df['credit_score'] >= mediana_score - 20),


        (df['employment_status'] == 'Unemployed') |
        (df['monthly_income_usd'] < mediana_renda * 0.6) |  # Limiar mais rigoroso
        (df['credit_score'] < mediana_score - 50)
    ]

    choices = [
        'Premium Elite', 'Premium Prime', 'Premium Emergent', 'Premium Traditional',
        'Standard Secure', 'Standard', 'Basic Stable', 'Basic Vulnerable'
    ]

    df['grupo_estrategico'] = np.select(conditions, choices, default='Standard')


    df.loc[df['grupo_estrategico'].str.startswith('Premium') &
           (df['credit_score'] < 600), 'grupo_estrategico'] = 'Standard Secure'

    return df