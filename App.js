import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack'; 

import LoginScreen from './screens/LoginScreen';
import RegisterScreen from './screens/RegisterScreen';
import RecoverScreen from './screens/RecoverScreen';
import MonitorScreen from './screens/MonitorScreen';

const Stack = createNativeStackNavigator();

export default function App() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName='Login'>
                <Stack.Screen name='Login' component={LoginScreen} options={{title: 'Login' }}/>
                <Stack.Screen name='Register' component={RegisterScreen} options={{title: 'Cadastro'}}/>
                <Stack.Screen name='Recover' component={RecoverScreen} options={{title: 'Recuperar senha'}}/>
                <Stack.Screen name='Monitoramento' component={MonitorScreen} options={{title: 'Monitoramento' }} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}