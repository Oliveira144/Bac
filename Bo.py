import streamlit as st
from collections import deque
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
        
        # Faz previsão automática após 5 jogadas
        if len(self.game_history) >= 5:
            self.last_prediction = self.predict_next()
            st.session_state.last_prediction = self.last_prediction
            
            # Atualiza estatísticas se não for a primeira previsão
            if len(self.game_history) > 5:
                self._update_stats(result)
                self._update_win_rate()

    def _update_win_rate(self):
        if self.prediction_stats['total'] > 0:
            self.prediction_stats['win_rate'] = round(
                (self.prediction_stats['wins'] / self.prediction_stats['total']) * 100, 1
            )

    def _update_stats(self, actual_result: str):
        if st.session_state.last_prediction['prediction'] == actual_result:
            self.prediction_stats['wins'] += 1
        self.prediction_stats['total'] += 1
        
        self.last_predictions.append({
            'predicted': st.session_state.last_prediction['prediction'],
            'actual': actual_result,
            'confidence': st.session_state.last_prediction['confidence']
        })

    def predict_next(self) -> Dict:
        if len(self.game_history) < 5:
            return {'prediction': None, 'confidence': 0, 'reason': 'Histórico insuficiente'}
        
        try:
            # 1. Análise Quântica
            quantum = self._analyze_quantum_pattern()
            
            # 2. Fibonacci Dinâmico
            fibonacci = self._analyze_dynamic_fibonacci()
            
            # 3. Pontos de Pressão
            pressure = self._analyze_pressure_points()
            
            # Combinação ponderada
            predictions = [
                {'method': quantum, 'weight': 0.45},
                {'method': fibonacci, 'weight': 0.35},
                {'method': pressure, 'weight': 0.20}
            ]
            
            valid_preds = [p for p in predictions if p['method']['prediction'] is not None]
            
            if not valid_preds:
                return self._smart_fallback()
            
            final_pred = self._aggregate_predictions(valid_preds)
            return self._apply_bayesian_correction(final_pred)
            
        except Exception as e:
            return {'prediction': None, 'confidence': 0, 'reason': f'Erro: {str(e)}'}

    def _analyze_quantum_pattern(self) -> Dict:
        last_15 = self.game_history[-15:]
        player_count = last_15.count('PLAYER')
        banker_count = last_15.count('BANKER')
        
        diff = abs(player_count - banker_count)
        if diff >= self.quantum_threshold:
            prediction = 'BANKER' if player_count > banker_count else 'PLAYER'
            return {
                'prediction': prediction,
                'confidence': min(90, 75 + diff * 2),
                'reason': f'Oscilação Quântica (Δ={diff})'
            }
        
        last_5 = last_15[-5:]
        if len(set(last_5)) == 1:
            return {
                'prediction': 'BANKER' if last_5[0] == 'PLAYER' else 'PLAYER',
                'confidence': 89,
                'reason': f'Entrelaçamento Quântico (5x {last_5[0]})'
            }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}

    def _analyze_dynamic_fibonacci(self) -> Dict:
        last_10 = self.game_history[-10:]
        numeric = [2 if x == 'PLAYER' else 3 if x == 'BANKER' else 5 for x in last_10]
        
        for i in range(len(self.fibonacci_sequence) - 2):
            fib_seq = self.fibonacci_sequence[i:i+3]
            if ','.join(map(str, fib_seq)) in ','.join(map(str, numeric)):
                next_val = self.fibonacci_sequence[i+3] if i+3 < len(self.fibonacci_sequence) else 3
                prediction = 'PLAYER' if next_val == 2 else 'BANKER' if next_val == 3 else 'TIE'
                return {
                    'prediction': prediction,
                    'confidence': 83 + (i * 2),
                    'reason': f'Fibonacci Dinâmico ({fib_seq})'
                }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}

    def _analyze_pressure_points(self) -> Dict:
        total = len(self.game_history)
        
        for point in self.pressure_points:
            if total % point == 0 and total >= point:
                last_n = self.game_history[-point:]
                p_count = last_n.count('PLAYER')
                b_count = last_n.count('BANKER')
                
                prediction = 'BANKER' if p_count > b_count else 'PLAYER'
                return {
                    'prediction': prediction,
                    'confidence': 85 + min(10, abs(p_count - b_count)),
                    'reason': f'Ponto de Pressão (múltiplo de {point})'
                }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}

    def _aggregate_predictions(self, predictions: List[Dict]) -> Dict:
        pred_counts = {}
        total_weight = 0
        
        for pred in predictions:
            method = pred['method']
            weight = pred['weight']
            
            if method['prediction'] not in pred_counts:
                pred_counts[method['prediction']] = {
                    'confidence': 0,
                    'reasons': [],
                    'weight': 0
                }
            
            pred_counts[method['prediction']]['confidence'] += method['confidence'] * weight
            pred_counts[method['prediction']]['reasons'].append(method['reason'])
            pred_counts[method['prediction']]['weight'] += weight
            total_weight += weight
        
        final_pred = max(pred_counts.items(), key=lambda x: x[1]['weight'])
        
        return {
            'prediction': final_pred[0],
            'confidence': final_pred[1]['confidence'] / final_pred[1]['weight'],
            'reason': ' | '.join(final_pred[1]['reasons'])
        }

    def _apply_bayesian_correction(self, prediction: Dict) -> Dict:
        if len(self.game_history) < 50:
            return prediction
        
        last_100 = self.game_history[-100:]
        p_ratio = last_100.count('PLAYER') / len(last_100)
        b_ratio = last_100.count('BANKER') / len(last_100)
        
        if prediction['prediction'] == 'PLAYER' and p_ratio > 0.52:
            return {
                **prediction,
                'confidence': max(75, prediction['confidence'] * 0.95),
                'reason': prediction['reason'] + ' | Correção Bayesiana (PLAYER super-representado)'
            }
        
        if prediction['prediction'] == 'BANKER' and b_ratio > 0.52:
            return {
                **prediction,
                'confidence': max(75, prediction['confidence'] * 0.95),
                'reason': prediction['reason'] + ' | Correção Bayesiana (BANKER super-representado)'
            }
        
        return prediction

    def _smart_fallback(self) -> Dict:
        last_10 = self.game_history[-10:]
        p_count = last_10.count('PLAYER')
        b_count = last_10.count('BANKER')
        
        if p_count < 3:
            return {'prediction': 'PLAYER', 'confidence': 65, 'reason': 'Correção: PLAYER sub-representado'}
        if b_count < 3:
            return {'prediction': 'BANKER', 'confidence': 65, 'reason': 'Correção: BANKER sub-representado'}
        
        return {'prediction': 'BANKER', 'confidence': 58, 'reason': 'Vantagem estatística padrão'}

    def get_stats(self) -> Dict:
        stats = {
            'win_rate': self.prediction_stats['win_rate'],
            'wins': self.prediction_stats['wins'],
            'total': self.prediction_stats['total'],
            'recent_predictions': list(self.last_predictions)
        }
        
        if stats['total'] > 10:
            last_10 = self.last_predictions[-10:]
            stats['recent_win_rate'] = round(
                sum(1 for p in last_10 if p['predicted'] == p['actual']) / len(last_10) * 100, 1
            ) if last_10 else 0
            
        return stats

    def reset(self):
        self.game_history = []
        self.prediction_stats = {'wins': 0, 'total': 0, 'win_rate': 0.0}
        self.last_predictions = deque(maxlen=20)
        if 'last_prediction' in st.session_state:
            del st.session_state.last_prediction

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
.stButton>button {
    height: 100px !important;
    width: 100% !important;
    font-size: 24px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    margin: 5px 0 !important;
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
.player-history {
    background-color: #3b82f6;
}
.banker-history {
    background-color: #ef4444;
}
.tie-history {
    background-color: #a855f7;
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
    
    # Botão PLAYER
    if st.button("🔵 PLAYER", key="player_btn", help="Clique para registrar vitória do Player"):
        st.session_state.predictor.add_result("PLAYER")
        st.rerun()
    
    # Botão BANKER
    if st.button("🔴 BANKER", key="banker_btn", help="Clique para registrar vitória do Banker"):
        st.session_state.predictor.add_result("BANKER")
        st.rerun()
    
    # Botão TIE
    if st.button("🟣 TIE", key="tie_btn", help="Clique para registrar um Tie"):
        st.session_state.predictor.add_result("TIE")
        st.rerun()

    # Botão de reset
    if st.button("🔄 Reiniciar Sistema", key="reset_btn", help="Limpa todo o histórico"):
        st.session_state.predictor.reset()
        st.rerun()

    # Histórico visual
    st.subheader("Histórico de Jogadas")
    if st.session_state.predictor.game_history:
        history_html = "<div class='history-container'>"
        for result in st.session_state.predictor.game_history:
            cls = "player-history" if result == "PLAYER" else "banker-history" if result == "BANKER" else "tie-history"
            history_html += f"<div class='history-item {cls}'>{result[0]}</div>"
        history_html += "</div>"
        st.markdown(history_html, unsafe_allow_html=True)
        st.caption(f"Total de jogos: {len(st.session_state.predictor.game_history)}")
    else:
        st.info("Nenhum resultado registrado ainda")

with col2:
    # Previsão automática
    if 'last_prediction' in st.session_state and st.session_state.last_prediction['prediction']:
        pred = st.session_state.last_prediction
        
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
st.caption("Sistema Bac Bo Predictor PRO v5.3 - © 2023 | Algoritmo: Análise Quântica + Fibonacci Dinâmico")

# Aplicar classes CSS específicas via JavaScript
st.markdown("""
<script>
// Aplica classes CSS aos botões
document.querySelector('button[title="Clique para registrar vitória do Player"]').classList.add('player-btn');
document.querySelector('button[title="Clique para registrar vitória do Banker"]').classList.add('banker-btn');
document.querySelector('button[title="Clique para registrar um Tie"]').classList.add('tie-btn');
document.querySelector('button[title="Limpa todo o histórico"]').classList.add('reset-btn');
</script>
""", unsafe_allow_html=True)
