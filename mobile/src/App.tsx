import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { HomeScreen } from './screens/HomeScreen';
import { SaleScreen } from './screens/SaleScreen';
import { SyncStatusBanner } from './components/SyncStatusBanner';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <SyncStatusBanner />
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Sale" component={SaleScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
