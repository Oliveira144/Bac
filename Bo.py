import numpy as np
from collections import deque
from typing import List, Dict, Optional, Tuple

class BacBoQuantumPredictor:
    def __init__(self, window_size: int = 100):
        self.game_history = []
        self.window_size = window_size
        self.prediction_stats = {'wins': 0, 'total': 0, 'win_rate': 0.0}
        self.last_predictions = deque(maxlen=20)
        
        # Parâmetros otimizados
        self.quantum_threshold = 7  # Reduzido para maior sensibilidade
        self.fibonacci_sequence = [2, 3, 5, 8, 13, 21, 34]  # Sequência estendida
        self.pressure_points = [5, 7, 10, 15, 20, 25, 30]  # Mais pontos de pressão
        self.min_history = 5  # Mínimo de jogadas para análise

    def add_result(self, result: str):
        """Adiciona um novo resultado ao histórico com validação"""
        result = result.upper()
        if result not in ['PLAYER', 'BANKER', 'TIE']:
            raise ValueError("Resultado inválido. Use 'PLAYER', 'BANKER' ou 'TIE'")
            
        self.game_history.append(result)
        
        # Atualiza estatísticas se houver uma previsão anterior
        if hasattr(self, 'last_prediction'):
            self._update_stats(result)
            self._update_win_rate()

    def _update_win_rate(self):
        """Atualiza a taxa de acerto automaticamente"""
        if self.prediction_stats['total'] > 0:
            self.prediction_stats['win_rate'] = (
                self.prediction_stats['wins'] / self.prediction_stats['total'] * 100
            )

    def predict_next(self) -> Dict:
        """Faz a previsão do próximo resultado com tratamento robusto"""
        if len(self.game_history) < self.min_history:
            return {
                'prediction': None,
                'confidence': 0,
                'reason': f'Histórico insuficiente (mínimo {self.min_history} jogadas)'
            }
        
        try:
            # 1. Análise Quântica Aprimorada
            quantum = self._analyze_quantum_pattern()
            
            # 2. Fibonacci Dinâmico com Memória
            fibonacci = self._analyze_dynamic_fibonacci()
            
            # 3. Pontos de Pressão com Peso Adaptativo
            pressure = self._analyze_pressure_points()
            
            # Combinação ponderada com pesos dinâmicos
            predictions = [
                {'method': quantum, 'weight': 0.45},
                {'method': fibonacci, 'weight': 0.35},
                {'method': pressure, 'weight': 0.20}
            ]
            
            # Filtra previsões válidas
            valid_preds = [p for p in predictions if p['method']['prediction'] is not None]
            
            if not valid_preds:
                return self._smart_fallback()
            
            # Agrega previsões com normalização
            final_pred = self._aggregate_predictions(valid_preds)
            
            # Aplica correção bayesiana com suavização
            final_pred = self._apply_bayesian_correction(final_pred)
            
            self.last_prediction = final_pred
            return final_pred
            
        except Exception as e:
            return {
                'prediction': None,
                'confidence': 0,
                'reason': f'Erro na análise: {str(e)}'
            }

    # [...] (Manter as outras funções como no código original, mas com tratamento de erros)

    def get_stats(self) -> Dict:
        """Retorna estatísticas de desempenho com verificação de segurança"""
        stats = {
            'win_rate': round(self.prediction_stats.get('win_rate', 0), 1),
            'wins': self.prediction_stats.get('wins', 0),
            'total': self.prediction_stats.get('total', 0),
            'recent_predictions': list(self.last_predictions)
        }
        
        # Adiciona análise de tendência
        if stats['total'] > 10:
            last_10 = self.last_predictions[-10:]
            stats['recent_win_rate'] = round(
                sum(1 for p in last_10 if p['predicted'] == p['actual']) / len(last_10) * 100, 1
            ) if last_10 else 0
            
        return stats

# Exemplo de uso completo e seguro
if __name__ == "__main__":
    print("=== BAC BO QUANTUM PREDICTOR ===")
    print("Sistema de previsão avançada (v4.1)\n")
    
    predictor = BacBoQuantumPredictor()
    
    # Simulação com dados de teste robustos
    test_data = [
        'PLAYER', 'BANKER', 'PLAYER', 'PLAYER', 'BANKER',
        'BANKER', 'BANKER', 'PLAYER', 'TIE', 'BANKER',
        'PLAYER', 'PLAYER', 'PLAYER', 'PLAYER', 'BANKER',
        'PLAYER', 'BANKER', 'BANKER', 'BANKER', 'BANKER'
    ]
    
    print("🔹 Simulando 20 jogadas...")
    for i, result in enumerate(test_data, 1):
        predictor.add_result(result)
        
        # Fazer previsão a cada 5 jogadas
        if i >= 5 and i % 5 == 0:
            prediction = predictor.predict_next()
            print(f"\n🎯 Jogo {i}:")
            print(f"Último resultado: {result}")
            print(f"Próxima aposta: {prediction['prediction']}")
            print(f"Confiança: {prediction['confidence']:.1f}%")
            print(f"Lógica: {prediction['reason']}")
    
    # Estatísticas finais com verificação completa
    stats = predictor.get_stats()
    print("\n📊 ESTATÍSTICAS FINAIS:")
    print(f"Taxa de acerto global: {stats['win_rate']:.1f}%")
    print(f"Acertos: {stats['wins']}/{stats['total']}")
    
    if 'recent_win_rate' in stats:
        print(f"Taxa de acerto recente (últimas 10): {stats['recent_win_rate']}%")
    
    print("\nÚltimas previsões:")
    for i, pred in enumerate(stats['recent_predictions'][-5:], 1):
        status = "✅" if pred['predicted'] == pred['actual'] else "❌"
        print(f"{i}. Previsto: {pred['predicted']} | Real: {pred['actual']} {status} | Conf: {pred['confidence']:.1f}%")
