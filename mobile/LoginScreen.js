// LoginScreen.js – extracted login view from App.js
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert, StyleSheet, StatusBar, LinearGradient } from 'react-native';
import { colors, gradients } from './theme';

export default function LoginScreen({ navigation }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    };

    const handleLogin = () => {
        if (!validateEmail(email)) {
            Alert.alert('Invalid Email', 'Please enter a valid email address.');
            return;
        }
        if (!password) {
            Alert.alert('Missing Password', 'Please enter your password.');
            return;
        }
        navigation.replace('Dashboard');
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <LinearGradient colors={gradients.background} style={styles.background} />
            <View style={styles.loginContainer}>
                <Text style={styles.loginTitle}>RegTech Login</Text>
                <Text style={styles.loginSubtitle}>Access your Compliance Dashboard</Text>
                <View style={styles.inputContainer}>
                    <TextInput
                        style={styles.input}
                        placeholder="Email Address"
                        placeholderTextColor="#a0aec0"
                        value={email}
                        onChangeText={setEmail}
                        autoCapitalize="none"
                        accessibilityLabel="Email input"
                        importantForAccessibility="yes"
                    />
                </View>
                <View style={styles.inputContainer}>
                    <TextInput
                        style={styles.input}
                        placeholder="Password"
                        placeholderTextColor="#a0aec0"
                        secureTextEntry={true}
                        value={password}
                        onChangeText={setPassword}
                        accessibilityLabel="Password input"
                        importantForAccessibility="yes"
                    />
                </View>
                <TouchableOpacity style={styles.loginBtn} onPress={handleLogin} accessibilityLabel="Sign In button">
                    <Text style={styles.loginBtnText}>Sign In</Text>
                </TouchableOpacity>
                <TouchableOpacity style={{ marginTop: 20 }}>
                    <Text style={{ color: '#00d2ff' }}>Forgot Password?</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: colors.backgroundStart },
    background: { position: 'absolute', left: 0, right: 0, top: 0, height: '100%' },
    loginContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 30 },
    loginTitle: { fontSize: 32, fontWeight: 'bold', color: '#fff', marginBottom: 10 },
    loginSubtitle: { fontSize: 16, color: '#a0aec0', marginBottom: 50 },
    inputContainer: { width: '100%', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: 12, borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)', marginBottom: 20 },
    input: { padding: 15, color: '#fff', fontSize: 16 },
    loginBtn: { width: '100%', backgroundColor: '#00d2ff', padding: 15, borderRadius: 12, alignItems: 'center', marginTop: 10 },
    loginBtnText: { color: '#0a0e17', fontSize: 18, fontWeight: 'bold' },
});
