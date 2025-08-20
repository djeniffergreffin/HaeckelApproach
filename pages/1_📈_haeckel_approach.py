import streamlit as st
import numpy as np
import pandas as pd
import warnings

st.set_page_config(page_title="Haeckel Approach", page_icon="📈", layout="wide")
st.sidebar.header("Haeckel Approach")
st.html(
    """
    <style>
        .haeckel-doc {
            width: 66.66%;
            max-width: none;
            margin: 0 auto;
            font-family: "Source Sans Pro", sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: var(--text-color, #262730);
        }

        .haeckel-doc h2,
        .haeckel-doc h3 {
            margin-top: 1.2em;
            color: inherit;
        }

        .haeckel-doc p,
        .haeckel-doc li {
            color: inherit;
        }

        .haeckel-doc ul,
        .haeckel-doc ol {
            padding-left: 1.2em;
        }

        .haeckel-doc code {
            background-color: rgba(200, 200, 200, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            color: inherit;
        }

        .haeckel-doc hr {
            border: none;
            border-top: 1px solid rgba(128, 128, 128, 0.3);
            margin: 1.5em 0;
        }

        @media (prefers-color-scheme: dark) {
            .haeckel-doc {
                color: #f5f5f5;
            }

            .haeckel-doc code {
                background-color: rgba(255, 255, 255, 0.1);
            }

            .haeckel-doc hr {
                border-top: 1px solid rgba(255, 255, 255, 0.2);
            }
        }
    </style>

    <div class="haeckel-doc">
        <h2>🧠 Abordagem de Haeckel</h2>
        <p>
            A <strong>Abordagem de Haeckel</strong> é um método matemático utilizado para estimar incertezas em medições ou concentrações com base em regressão linear e estatísticas associadas.
            Ela é especialmente útil em contextos laboratoriais e analíticos onde é necessário calcular intervalos de confiança e incertezas expandidas de forma robusta.
        </p>
        <hr />
        <h3>📥 Entradas</h3>
        <ul>
            <li><code>LI</code> – <strong>Limite Inferior</strong>: valor mínimo da concentração ou faixa de interesse. Se não informado, será 15% do <code>LS</code>.</li>
            <li><code>LS</code> – <strong>Limite Superior</strong>: valor máximo da concentração. Obrigatório.</li>
            <li><code>xi</code> – <strong>Concentrações específicas</strong>: lista opcional de valores para cálculo de incertezas. Se omitido, será usado <code>Med</code>.</li>
        </ul>
        <h3>⚙️ Etapas do Cálculo</h3>
        <ol>
            <li><strong>Mediana (Med):</strong> <code>(LI + LS) / 2</code></li>
            <li><strong>DPE_ln:</strong> desvio padrão estimado com base em distribuição log-normal</li>
            <li><strong>CVE*:</strong> Coeficiente de Variação com base em DPE_ln</li>
            <li><strong>Regressão Linear:</strong> cálculo de <code>Slope</code> e <code>Intercept</code></li>
            <li><strong>Para cada <code>xi</code>:</strong> cálculo de:
                <ul>
                    <li><code>pDPA_xi</code>, <code>pCVA_xi</code>, <code>pBxi</code>, <code>pUc_xi</code></li>
                    <li><code>pU_Unilateral</code>, <code>pU_Bilateral</code></li>
                    <li><code>pUAEQ90</code>, <code>pUAEQ95</code></li>
                    <li><code>pETM_Unilateral</code>, <code>pETM_Bilateral</code></li>
                </ul>
            </li>
        </ol>
        <h3>📊 Saídas</h3>
        <ul>
            <li><strong>Resultados Principais:</strong> tabela com valores fixos como <code>LI</code>, <code>LS</code>, <code>Med</code>, etc.</li>
            <li><strong>Resultados por Concentração (xi):</strong> tabela com colunas para cada xi e os cálculos associados.</li>
        </ul>
        <h3>✅ Aplicações</h3>
        <p>
            Utilizada para validação, controle de qualidade e avaliação de incertezas em análises laboratoriais.
        </p>
    </div>
    """
)



with st.sidebar:
    input_li = st.number_input('**Enter the lower limit number**', min_value=None, max_value=None, format="%0.3f")
    input_ls = st.number_input('**Enter the upper limit number**', min_value=0.000, max_value=None, format="%0.3f")
    number_CCT = st.number_input('**Enter the number of concentrations**', min_value=0, max_value=5)
    if number_CCT == 1:
        cct_1 = st.number_input(label='**Enter the concentration value below**',min_value=0.0000 ,format="%.f", key=1)
    elif number_CCT == 2:
        cct_1 = st.number_input(label='**Enter the concentration value below**',min_value=0.0000 ,format="%.f",key=2)
        cct_2 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f", key=3)
    elif number_CCT == 3:
        cct_1 = st.number_input(label='**Enter the concentration value below**',min_value=0.0000 ,format="%.f",key=4)
        cct_2 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f", key=5)
        cct_3 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f", key=6)
    elif number_CCT == 4:
        cct_1 = st.number_input(label='**Enter the concentration value below**',min_value=0.0000 ,format="%.f",key=7)
        cct_2 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f", key=8)
        cct_3 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f",key=9)
        cct_4 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f", key=10)
    elif number_CCT == 5:
        cct_1 = st.number_input(label='**Enter the concentration value below**',min_value=0.0000 ,format="%.f",key=11)
        cct_2 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f", key=12)
        cct_3 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f",key=13)
        cct_4 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f", key=14)
        cct_5 = st.number_input(label=" ",label_visibility='collapsed',min_value=0.0000 ,format="%.f",key=15)
    
    analyze_button = st.button('**:green[Calcular]**')
    st.info('*Developed by <djeniffer.greffin@gmail.com>')

if analyze_button:
    try:
        input_xi = None
        if number_CCT == 1:
            input_xi = [cct_1]
        elif number_CCT == 2:
            input_xi = [cct_1,cct_2]
        elif number_CCT == 3:
            input_xi = [cct_1,cct_2,cct_3]
        elif number_CCT == 4:
            input_xi = [cct_1,cct_2,cct_3,cct_4]
        elif number_CCT == 5:
            input_xi = [cct_1,cct_2,cct_3,cct_4,cct_5]
        else:
            input_xi = [None]
        def haeckel_approach(li_ir, ls_ir, xi=None, decimals=2):
            def is_empty(x):
                if x is None:
                    return True
                if isinstance(x, (str, list, np.ndarray, pd.Series, tuple)):
                    return len(x) == 0
                return False

            if is_empty(ls_ir):
                raise ValueError("Upper limit is required and cannot be empty.")

            ls = np.asarray(ls_ir, dtype=float)
            if ls.ndim == 0:
                ls = np.array([ls])
            if np.any(np.isnan(ls)):
                raise ValueError("Upper limit cannot contain NaN values.")
            if np.any(ls <= 0):
                raise ValueError("Upper limit must be greater than zero.")

            if is_empty(li_ir):
                li = 0.15 * ls
            else:
                li = np.asarray(li_ir, dtype=float)
                if li.ndim == 0:
                    li = np.array([li])
                li, ls = np.broadcast_arrays(li, ls)
                li = np.where((np.isnan(li) | (li <= 0)), 0.15 * ls, li)

            mask_bad = ls < li
            if np.any(mask_bad):
                warnings.warn("Upper limit < Lower limit in some cases. Results will be NaN.")
                li[mask_bad] = np.nan
                ls[mask_bad] = np.nan

            DPE_ln = (np.log(ls) - np.log(li)) / 3.92
            CVE_star = np.sqrt(np.exp(DPE_ln ** 2) - 1)
            pCV_A = np.sqrt(np.maximum((CVE_star * 100) - 0.25, 0)) / 100
            Med_ln = (np.log(ls) + np.log(li)) / 2
            Med = np.exp(Med_ln)
            pS_A_Med = pCV_A * Med
            Intercept = 0.20 * pS_A_Med
            Slope = (pS_A_Med - Intercept) / Med
            if is_empty(li_ir):
                pS_A_LI = "---"
                pD_LI = "---"
            else:
                pS_A_LI = li_ir * Slope + Intercept
                pD_LI = np.round(1.645 * pS_A_LI, decimals)

            pS_A_LS = ls * Slope + Intercept
            pD_LS = np.round(1.645 * pS_A_LS, decimals)

            df_base = pd.DataFrame({
                "LI": li,
                "LS": ls,
                "Med": Med,
                "DPE_ln": DPE_ln,
                "CVE_star": CVE_star,
                "pCV_A": pCV_A,
                "pS_A.Med": pS_A_Med,
                "Slope": Slope,
                "Intercept": Intercept,
                "pS_A.LI": pS_A_LI,
                "pS_A.LS": pS_A_LS,
                "pD_LI": pD_LI,
                "pD_LS": pD_LS,
            }).transpose().reset_index()
            df_base.columns = ["Variable", "Value"]
            st.subheader("📊 Main Results")
            df_base_html = df_base.to_html(index=False, border=1, classes="custom-table")
            st.html(f"""
                        <style>
                            .custom-table {{
                                width: 100%;
                                border-collapse: collapse;
                                table-layout: fixed;
                            }}
                            .custom-table th {{
                                background-color: #f0f2f6;
                                color: #000;
                                padding: 10px 20px;
                                border: 1px solid #ddd;
                                text-align: center;
                                min-width: 140px;
                            }} 
                            .custom-table td {{
                                padding: 10px 20px;
                                border: 1px solid #ddd;
                                text-align: center;
                                word-wrap: break-word;
                                min-width: 140px;
                            }}
                            .custom-table th:nth-child(1),
                            .custom-table td:nth-child(1) {{
                                width: 200px;
                            }}
                            .custom-table th:nth-child(2),
                            .custom-table td:nth-child(2) {{
                                width: 150px;
                            }}
                        </style>
                        <div style="max-width: 700px; margin: 0 auto; font-family: sans-serif;">
                            {df_base_html}
                        </div>
                    """)
            st.markdown("---")
            
            if xi is None:
                xi = []
            elif not isinstance(xi, list):
                raise ValueError("xi deve ser uma lista (ex.: xi=[valor1, valor2, ...])")
            xi = [v for v in xi if v is not None]
            if len(xi) > 5:
                raise ValueError("xi pode conter no máximo 5 valores.")
            if len(xi) == 0:
                xi = [Med.astype(float)]
            resultados_xi = {
                "pDPA_xi": [],
                "pCVA_xi": [],
                "pB_xi": [],
                "pUc_xi": [],
                "pU_Unilateral_xi": [],
                "pU_Bilateral_xi": [],
                "pUAEQ90_xi": [],
                "pUAEQ95_xi": [],
                "pETM_Unilateral_xi": [],
                "pETM_Bilateral_xi": [],
            }
            
            st.subheader("🔍 Results by Concentration")
            
            for i, item_xi in enumerate(xi):
                pDPA_xi = item_xi * Slope + Intercept
                pCVA_xi = pDPA_xi / item_xi
                pB_xi = 0.7 * pCVA_xi
                pUc_xi = np.sqrt(pCVA_xi**2 + pB_xi**2)
                pU_Unilateral_xi = 1.645 * pUc_xi
                pU_Bilateral_xi  = 1.96  * pUc_xi
                pUAEQ90_xi = 1.645 * pU_Bilateral_xi
                pUAEQ95_xi = 1.96  * pU_Bilateral_xi
                pETM_Unilateral_xi = 1.645 * pCVA_xi + pB_xi
                pETM_Bilateral_xi = 1.96 * pCVA_xi + pB_xi

                resultados_xi["pDPA_xi"].append(pDPA_xi)
                resultados_xi["pCVA_xi"].append(pCVA_xi)
                resultados_xi["pB_xi"].append(pB_xi)
                resultados_xi["pUc_xi"].append(pUc_xi)
                resultados_xi["pU_Unilateral_xi"].append(pU_Unilateral_xi)
                resultados_xi["pU_Bilateral_xi"].append(pU_Bilateral_xi)
                resultados_xi["pUAEQ90_xi"].append(pUAEQ90_xi)
                resultados_xi["pUAEQ95_xi"].append(pUAEQ95_xi)
                resultados_xi["pETM_Unilateral_xi"].append(pETM_Unilateral_xi)
                resultados_xi["pETM_Bilateral_xi"].append(pETM_Bilateral_xi)

            df_xi = pd.DataFrame(resultados_xi).transpose().reset_index()
            if len(xi) == 1 and np.allclose(xi[0], Med.astype(float)):
                df_xi.columns = ["Variable", "Value"]
            else:
                df_xi.columns = ["Variable"] + [f"Value (xi = {float(x):,.2f})" for x in xi]
            for col in df_xi.columns[1:]:
                df_xi[col] = df_xi[col].apply(lambda x: float(x[0]) if isinstance(x, (np.ndarray, list)) else float(x))
            df_xi_html = df_xi.to_html(index=False, classes="custom-table-xi")
            st.html(
                    f"""
                    <style>
                        .custom-table-xi {{
                            width: 100%;
                            border-collapse: collapse;
                            table-layout: auto;
                            font-family: "Source Sans Pro", sans-serif;
                            font-size: 16px;
                        }}
                        .custom-table-xi th {{
                            background-color: #f0f2f6;
                            color: #000;
                            padding: 10px 20px;
                            border: 1px solid #ddd;
                            text-align: center;
                            min-width: 140px;
                        }}
                        .custom-table-xi td {{
                            padding: 10px 20px;
                            border: 1px solid #ddd;
                            text-align: center;
                            word-wrap: break-word;
                            min-width: 140px;
                        }}
                        .custom-table-xi td:first-child {{
                            text-align: left;
                            font-weight: bold;
                            min-width: 180px;
                        }}
                        .table-container-xi {{
                            display: flex;
                            justify-content: center;
                            overflow-x: auto;
                            padding-bottom: 10px;
                        }}
                    </style>
                    <div class="table-container-xi">
                        {df_xi_html}
                    </div>
                    """,
                )

        haeckel_approach(input_li, input_ls, input_xi, decimals=2)
    except ValueError as error:
        print("ValueError occurred:", error)
        #st.write(error)
        st.error('Inappropriate value was entered.', icon="❗")
    except TypeError as error:
        #st.write(error)
        st.error('Your data includes non-numerical types of entry. Please check your data.', icon="❗")
    except Exception as error:
        #st.write(error)
        st.error(f"Ocorreu um erro inesperado: {error}", icon="🚨")
