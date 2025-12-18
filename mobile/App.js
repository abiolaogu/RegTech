```javascript
// App.js – Refactored with AuthContext and React Navigation
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { AuthProvider } from './AuthContext';
import SettingsScreen from './SettingsScreen';
import { colors, gradients } from './theme';
import { StyleSheet, View, StatusBar } from 'react-native'; // Removed LinearGradient from here as it's not used in this App.js
import LoginScreen from './LoginScreen';
import DashboardScreen from './DashboardScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <AuthProvider>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Dashboard" component={DashboardScreen} />
          <Stack.Screen name="Settings" component={SettingsScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </AuthProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.backgroundStart,
  },
  background: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    height: '100%',
  },
    loginContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 30,
    },
    loginTitle: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#fff',
        marginBottom: 10,
    },
    loginSubtitle: {
        fontSize: 16,
        color: '#a0aec0',
        marginBottom: 50,
    },
    inputContainer: {
        width: '100%',
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: 12,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
        marginBottom: 20,
    },
    input: {
        padding: 15,
        color: '#fff',
        fontSize: 16,
    },
    loginBtn: {
        width: '100%',
        backgroundColor: '#00d2ff',
        padding: 15,
        borderRadius: 12,
        alignItems: 'center',
        marginTop: 10,
    },
    loginBtnText: {
        color: '#0a0e17',
        fontSize: 18,
        fontWeight: 'bold',
    },
    // App Styles
    header: {
        marginTop: 50,
        paddingHorizontal: 20,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    headerTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#fff',
    },
    avatar: {
        width: 35,
        height: 35,
        borderRadius: 20,
        backgroundColor: '#3a7bd5',
    },
    content: {
        flex: 1,
        padding: 20,
    },
    sectionTitle: {
        fontSize: 18,
        color: '#a0aec0',
        marginTop: 20,
        marginBottom: 10,
        fontWeight: '600',
    },
    card: {
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: 16,
        padding: 20,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    alertCard: {
        borderColor: '#ff4d4d',
        backgroundColor: 'rgba(255, 77, 77, 0.05)',
    },
    cardHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 8,
    },
    cardTitle: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
    badgeRed: {
        color: '#ff4d4d',
        fontWeight: 'bold',
        fontSize: 12,
    },
    cardText: {
        color: '#ccc',
        fontSize: 14,
        marginBottom: 12,
    },
    actionBtn: {
        backgroundColor: '#ff4d4d',
        padding: 10,
        borderRadius: 8,
        alignItems: 'center',
    },
    actionBtnText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    grid: {
        flexDirection: 'row',
        gap: 15,
    },
    gridItem: {
        flex: 1,
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: 16,
        padding: 15,
        alignItems: 'center',
    },
    gridLabel: {
        color: '#a0aec0',
        fontSize: 12,
    },
    gridValue: {
        color: '#fff',
        fontSize: 24,
        fontWeight: 'bold',
        marginVertical: 5,
    },
    gridStatusOK: {
        color: '#00fa9a',
        fontSize: 12,
        fontWeight: 'bold',
    },
    gridStatusWarn: {
        color: '#ffd700',
        fontSize: 12,
        fontWeight: 'bold',
    },
    taskTitle: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
    taskSub: {
        color: '#a0aec0',
        fontSize: 12,
        marginBottom: 12,
    },
    biometricBtn: {
        borderColor: '#00d2ff',
        borderWidth: 1,
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
    },
    biometricText: {
        color: '#00d2ff',
        fontWeight: 'bold',
    },
    bottomNav: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        padding: 20,
        backgroundColor: 'rgba(0,0,0,0.5)',
        borderTopWidth: 1,
        borderTopColor: 'rgba(255,255,255,0.1)'
    },
    navItem: {
        color: '#a0aec0',
        fontWeight: '600',
    },
    navItemActive: {
        color: '#00d2ff',
        fontWeight: 'bold',
    }

});
