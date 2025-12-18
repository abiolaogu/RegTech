// SettingsScreen.js – simple settings view
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, StatusBar, LinearGradient } from 'react-native';
import { colors, gradients } from './theme';
import { useAuth } from './AuthContext';

export default function SettingsScreen({ navigation }) {
    const { logout } = useAuth();

    const handleLogout = () => {
        logout();
        navigation.replace('Login');
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <LinearGradient colors={gradients.background} style={styles.background} />
            <View style={styles.content}>
                <Text style={styles.title}>Settings</Text>
                {/* Add settings options here */}
                <TouchableOpacity style={styles.button} onPress={handleLogout} accessibilityLabel="Logout button">
                    <Text style={styles.buttonText}>Logout</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: colors.backgroundStart },
    background: { position: 'absolute', left: 0, right: 0, top: 0, height: '100%' },
    content: { flex: 1, justifyContent: 'center', alignItems: 'center' },
    title: { fontSize: 28, fontWeight: 'bold', color: '#fff', marginBottom: 20 },
    button: { backgroundColor: '#ff4d4d', paddingVertical: 12, paddingHorizontal: 30, borderRadius: 8 },
    buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
});
