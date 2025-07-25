import streamlit as st
from collections import deque
import numpy as np
from typing import List, Dict

class BacBoPredictor:
    def __init__(self):
        self.game_history = []
        self.prediction_stats = {'wins': 0, 'total': 0, 'win_rate': 0.0}
        self.last_predictions = deque(maxlen=20)
        self.quantum_threshold = 7
        self.fibonacci_sequence = [2, 3, 5, 8, 13, 21, 34]
        self.pressure_points = [5, 7, 10, 15, 20, 25, 30]

    def add_result(self, result: str):
        result = result.upper()
        if result not in ['PLAYER', 'BANKER', 'TIE']:
            raise ValueError("Resultado inválido")
        self.game_history.append(result)
        
        if len(self.game_history) >= 5:
            self.last_prediction = self.predict_next()
            
            if len(self.game_history) > 5:
                self._update_stats(result)
                self._update_win_rate()

    # [...] (Manter todas as outras funções da classe BacBoPredictor como antes)

# Configuração do Streamlit
st.set_page_config(
    page_title="Bac Bo Predictor PRO",
    page_icon="🎲",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
/* Botões grandes */
.big-button {
    height: 100px;
    font-size: 24px !important;
    font-weight: bold !important;
    margin: 5px;
    border-radius: 10px !important;
}
.player-btn {
    background-color: #3b82f6 !important;
    color: white !important;
}
.banker-btn {
    background-color: #ef4444 !important;
    color: white !important;
}
.tie-btn {
    background-color: #a855f7 !important;
    color: white !important;
}
.reset-btn {
    background-color: #64748b !important;
    color: white !important;
}

/* Histórico em bolinhas */
.history-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 20px 0;
}
.history-item {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Cartão de previsão */
.prediction-card {
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    border-left: 6px solid;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.high-confidence {
    border-color: #10b981;
    background: linear-gradient(90deg, #064e3b10 0%, #064e3b05 100%);
}
.medium-confidence {
    border-color: #f59e0b;
    background: linear-gradient(90deg, #92400e10 0%, #92400e05 100%);
}
.low-confidence {
    border-color: #ef4444;
    background: linear-gradient(90deg, #7f1d1d10 0%, #7f1d1d05 100%);
}
</style>
""", unsafe_allow_html=True)

# Inicialização do predictor
if 'predictor' not in st.session_state:
    st.session_state.predictor = BacBoPredictor()

# Layout principal
st.title("🎲 BAC BO PREDICTOR PRO")
st.markdown("Sistema automático com botões intuitivos e histórico visual")

# Coluna principal
col1, col2 = st.columns([3, 2])

with col1:
    # Seção de botões grandes
    st.subheader("Registrar Resultado")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("🔵 PLAYER", key="player_btn", help="Clique para registrar vitória do Player", 
                    type="primary", class_name="big-button player-btn"):
            st.session_state.predictor.add_result("PLAYER")
            st.rerun()
    
    with btn_col2:
        if st.button("🔴 BANKER", key="banker_btn", help="Clique para registrar vitória do Banker", 
                    type="primary", class_name="big-button banker-btn"):
            st.session_state.predictor.add_result("BANKER")
            st.rerun()
    
    with btn_col3:
        if st.button("🟣 TIE", key="tie_btn", help="Clique para registrar um Tie", 
                    type="primary", class_name="big-button tie-btn"):
            st.session_state.predictor.add_result("TIE")
            st.rerun()

    # Botão de reset
    if st.button("🔄 Reiniciar Sistema", key="reset_btn", help="Limpa todo o histórico",
                type="secondary", class_name="big-button reset-btn"):
        st.session_state.predictor.reset()
        st.rerun()

    # Histórico visual
    st.subheader("Histórico de Jogadas")
    if st.session_state.predictor.game_history:
        history_html = "<div class='history-container'>"
        for result in st.session_state.predictor.game_history:
            cls = "player" if result == "PLAYER" else "banker" if result == "BANKER" else "tie"
            history_html += f"<div class='history-item {cls}'>{result[0]}</div>"
        history_html += "</div>"
        st.markdown(history_html, unsafe_allow_html=True)
        st.caption(f"Total de jogos: {len(st.session_state.predictor.game_history)}")
    else:
        st.info("Nenhum resultado registrado ainda")

with col2:
    # Previsão automática
    if len(st.session_state.predictor.game_history) >= 5 and hasattr(st.session_state.predictor, 'last_prediction'):
        pred = st.session_state.predictor.last_prediction
        if pred['prediction']:
            # Determina estilo baseado na confiança
            if pred['confidence'] >= 75:
                confidence_class = "high-confidence"
                confidence_level = "ALTA CONFIANÇA"
                confidence_emoji = "🔥"
            elif pred['confidence'] >= 60:
                confidence_class = "medium-confidence"
                confidence_level = "MÉDIA CONFIANÇA"
                confidence_emoji = "⚡"
            else:
                confidence_class = "low-confidence"
                confidence_level = "BAIXA CONFIANÇA"
                confidence_emoji = "💡"
            
            # Cor do texto
            pred_color = "#3b82f6" if pred['prediction'] == "PLAYER" else "#ef4444" if pred['prediction'] == "BANKER" else "#a855f7"
            
            st.markdown(f"""
            <div class="prediction-card {confidence_class}">
                <h2 style="margin-top:0;color:{pred_color};">PRÓXIMA APOSTA: {pred['prediction']}</h2>
                <p style="font-size:18px;"><strong>{confidence_emoji} Confiança:</strong> <span style="color:{pred_color}">{pred['confidence']:.1f}%</span> ({confidence_level})</p>
                <p style="font-size:16px;"><strong>📊 Lógica:</strong> {pred['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Estatísticas
    stats = st.session_state.predictor.get_stats()
    if stats['total'] > 0:
        st.subheader("📈 Estatísticas")
        
        st.metric("Taxa de Acerto Global", f"{stats['win_rate']:.1f}%", 
                 help="Porcentagem de previsões corretas desde o início")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Previsões Corretas", stats['wins'])
        with col_stat2:
            st.metric("Total de Previsões", stats['total'])
        
        if 'recent_win_rate' in stats:
            st.metric("Acerto Recente (últimas 10)", f"{stats['recent_win_rate']:.1f}%",
                     help="Taxa de acerto das últimas 10 previsões")

# Rodapé
st.markdown("---")
st.caption("Sistema Bac Bo Predictor PRO v5.2 - © 2023 | Algoritmo: Análise Quântica + Fibonacci Dinâmico")
