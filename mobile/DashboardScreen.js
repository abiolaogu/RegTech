// DashboardScreen.js – main dashboard view extracted from App.js
import React from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, StatusBar, LinearGradient } from 'react-native';
import { colors, gradients } from './theme';

const alerts = [{ id: '1', title: 'CBN High Alert', badge: 'URGENT', message: '4 Potential AML Flags detected in last hour.' }];
const tasks = [{ id: '1', title: 'Sign Mid-Year Report', sub: 'Due in 3 days' }];

export default function DashboardScreen({ navigation }) {
    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <LinearGradient colors={gradients.background} style={styles.background} />

            {/* Header */}
            <View style={styles.header}>
                <Text style={styles.headerTitle}>RegTech Mobile</Text>
                <TouchableOpacity style={styles.profileBtn} onPress={() => navigation.navigate('Settings')}>
                    <View style={styles.avatar} />
                </TouchableOpacity>
            </View>

            {/* Content */}
            <View style={styles.content}>
                {/* Alerts Section */}
                <Text style={styles.sectionTitle}>Priority Alerts</Text>
                <FlatList
                    data={alerts}
                    keyExtractor={item => item.id}
                    renderItem={({ item }) => (
                        <View style={[styles.card, styles.alertCard]}>
                            <View style={styles.cardHeader}>
                                <Text style={styles.cardTitle}>{item.title}</Text>
                                <Text style={styles.badgeRed}>{item.badge}</Text>
                            </View>
                            <Text style={styles.cardText}>{item.message}</Text>
                            <TouchableOpacity style={styles.actionBtn} accessibilityLabel="Review Now button">
                                <Text style={styles.actionBtnText}>Review Now</Text>
                            </TouchableOpacity>
                        </View>
                    )}
                />

                {/* Quick Stats Grid */}
                <Text style={styles.sectionTitle}>Compliance Pulse</Text>
                <View style={styles.grid}>
                    <View style={styles.gridItem}>
                        <Text style={styles.gridLabel}>NCC Levy</Text>
                        <Text style={styles.gridValue}>N452M</Text>
                        <Text style={styles.gridStatusWarn}>Pending</Text>
                    </View>
                    <View style={styles.gridItem}>
                        <Text style={styles.gridLabel}>FCC 477</Text>
                        <Text style={styles.gridValue}>98.5%</Text>
                        <Text style={styles.gridStatusOK}>Sent</Text>
                    </View>
                </View>

                {/* Pending Actions */}
                <Text style={styles.sectionTitle}>My Tasks</Text>
                <FlatList
                    data={tasks}
                    keyExtractor={item => item.id}
                    renderItem={({ item }) => (
                        <View style={styles.card}>
                            <Text style={styles.taskTitle}>{item.title}</Text>
                            <Text style={styles.taskSub}>{item.sub}</Text>
                            <TouchableOpacity style={styles.biometricBtn} accessibilityLabel="Tap to Sign button">
                                <Text style={styles.biometricText}>Tap to Sign (Biometric)</Text>
                            </TouchableOpacity>
                        </View>
                    )}
                />
            </View>

            {/* Bottom Nav */}
            <View style={styles.bottomNav}>
                <Text style={styles.navItemActive}>Home</Text>
                <Text style={styles.navItem}>Alerts</Text>
                <Text style={styles.navItem}>Profile</Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: colors.backgroundStart },
    background: { position: 'absolute', left: 0, right: 0, top: 0, height: '100%' },
    // Reuse styles from App.js (you may import a shared style file later)
});
