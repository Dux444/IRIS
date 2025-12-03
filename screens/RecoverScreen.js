import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import api from '../services/api';

export default function RecoverScreen({ navigation }) {
  const [usuario, setUsuario] = useState('');
  const [novaSenha, setNovaSenha] = useState('');

  const handleRecover = async () => {
    try {
      const response = await api.post('/recover', { nome: usuario, nova_senha: novaSenha });
      Alert.alert('Sucesso', response.data.message);
      navigation.goBack();
    } catch (error) {
      Alert.alert('Erro', error.response?.data?.error || 'Falha ao recuperar senha');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Recuperar Senha</Text>

      <TextInput
        placeholder="Usuário"
        value={usuario}
        onChangeText={setUsuario}
        style={styles.input}
      />

      <TextInput
        placeholder="Nova Senha"
        secureTextEntry
        value={novaSenha}
        onChangeText={setNovaSenha}
        style={styles.input}
      />

      <TouchableOpacity style={styles.button} onPress={handleRecover}>
        <Text style={styles.buttonText}>Atualizar Senha</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.goBack()}>
        <Text style={styles.linkText}>Voltar ao login</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#1C1C1C',
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#FFF',
    textAlign: 'center',
    marginBottom: 25,
  },
  input: {
    borderWidth: 1,
    borderColor: '#888',
    borderRadius: 10,
    padding: 10,
    marginBottom: 15,
    backgroundColor: '#FFF',
  },
  button: {
    backgroundColor: '#F39C12',
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
    marginBottom: 15,
  },
  buttonText: { color: '#FFF', fontSize: 18, fontWeight: 'bold' },
  linkText: {
    color: '#2E86DE',
    fontSize: 16,
    textAlign: 'center',
    textDecorationLine: 'underline',
  },
});
