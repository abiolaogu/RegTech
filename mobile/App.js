import React from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, StatusBar } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { BlurView } from 'expo-blur';

export default function App() {
    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <LinearGradient
                colors={['#0a0e17', '#1a202c']}
                style={styles.background}
            />

            {/* Header */}
            <View style={styles.header}>
                <Text style={styles.headerTitle}>RegTech Mobile</Text>
                <TouchableOpacity style={styles.profileBtn}>
                    <View style={styles.avatar} />
                </TouchableOpacity>
            </View>

            <ScrollView style={styles.content}>

                {/* Alerts Section */}
                <Text style={styles.sectionTitle}>Priority Alerts</Text>
                <View style={[styles.card, styles.alertCard]}>
                    <View style={styles.cardHeader}>
                        <Text style={styles.cardTitle}>CBN High Alert</Text>
                        <Text style={styles.badgeRed}>URGENT</Text>
                    </View>
                    <Text style={styles.cardText}>4 Potential AML Flags detected in last hour.</Text>
                    <TouchableOpacity style={styles.actionBtn}>
                        <Text style={styles.actionBtnText}>Review Now</Text>
                    </TouchableOpacity>
                </View>

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
                <View style={styles.card}>
                    <Text style={styles.taskTitle}>Sign Mid-Year Report</Text>
                    <Text style={styles.taskSub}>Due in 3 days</Text>
                    <TouchableOpacity style={styles.biometricBtn}>
                        <Text style={styles.biometricText}>Tap to Sign (Biometric)</Text>
                    </TouchableOpacity>
                </View>

            </ScrollView>

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
    container: {
        flex: 1,
        backgroundColor: '#0a0e17',
    },
    background: {
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        height: '100%',
    },
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
