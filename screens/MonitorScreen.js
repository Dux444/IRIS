import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { WebView } from 'react-native-webview';
import api from '../services/api';

// Definindo o IP fixo que é o seu endereço de rede atual
const YOUR_CURRENT_IP = '192.168.0.6';
const VIDEO_STREAM_URL = `http://${YOUR_CURRENT_IP}:5001/video_feed`;


export default function MonitorScreen({ navigation }) {
  const [monitoramento, setMonitoramento] = useState(false);
  const [loading, setLoading] = useState(false);

  const iniciarMonitoramento = async () => {
    try {
      setLoading(true);
      // O 'api.post' usa a porta 5000, que será corrigida no api.js
      await api.post('/start'); 
      setMonitoramento(true);
    } catch (error) {
      console.error('Erro ao iniciar monitoramento:', error);
    } finally {
      setLoading(false);
    }
  };

  const pararMonitoramento = async () => {
    try {
      await api.post('/stop');
      setMonitoramento(false);
    } catch (error) {
      console.error('Erro ao parar monitoramento:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Central de Monitoramento</Text>

      {loading ? (
        <ActivityIndicator size="large" color="#00ff88" />
      ) : monitoramento ? (
        <View style={styles.videoContainer}>
          <WebView
            // URL CORRIGIDA: Usa o IP 192.168.0.6 e a porta 5001
            source={{ uri: VIDEO_STREAM_URL }} 
            style={styles.video}
            allowsFullscreenVideo={true}
            mediaPlaybackRequiresUserAction={false}
            javaScriptEnabled={true}
            domStorageEnabled={true}
            // Adicionando um fallback de erro para melhor diagnóstico:
            onError={(syntheticEvent) => {
              const { nativeEvent } = syntheticEvent;
              console.error('WebView error:', nativeEvent.description, 'Code:', nativeEvent.code);
            }}
          />
        </View>
      ) : (
        <Text style={styles.status}>Monitoramento parado</Text>
      )}

      <TouchableOpacity style={[styles.button, styles.start]} onPress={iniciarMonitoramento}>
        <Text style={styles.buttonText}>Iniciar Monitoramento</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.button, styles.stop]} onPress={pararMonitoramento}>
        <Text style={styles.buttonText}>Parar Monitoramento</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.button, styles.report]}
        onPress={() => navigation.navigate('Relatórios')}>
        <Text style={styles.buttonText}>Ver Relatórios</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#FFF',
    marginBottom: 15,
  },
  status: {
    color: '#AAA',
    marginBottom: 25,
    fontSize: 16,
  },
  videoContainer: {
    width: '100%',
    height: 400,
    marginBottom: 20,
    borderRadius: 10,
    overflow: 'hidden',
  },
  video: {
    flex: 1,
  },
  button: {
    width: '80%',
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: 'center',
    marginVertical: 8,
  },
  start: {
    backgroundColor: '#2ECC71',
  },
  stop: {
    backgroundColor: '#E74C3C',
  },
  report: {
    backgroundColor: '#3498DB',
  },
  buttonText: {
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 16,
  },
});