import * as Device from 'expo-device';
import { Button, Platform, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { AnimatedIcon } from '@/components/animated-icon';
import { HintRow } from '@/components/hint-row';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { WebBadge } from '@/components/web-badge';
import { BottomTabInset, MaxContentWidth, Spacing } from '@/constants/theme';
import { useNavigation } from '@react-navigation/native';
import React from 'react';
import { TextInput } from 'react-native';
// import DatePicker from 'react-native-date-picker';
import DateTimePicker from '@react-native-community/datetimepicker';
import { supabase } from '../../lib/supabase';



function getDevMenuHint() {

  

  const navigation = useNavigation();
    
      
  if (Platform.OS === 'web') {
    return <ThemedText type="small">use browser devtools</ThemedText>;
  }
  if (Device.isDevice) {
    return (
      <ThemedText type="small">
        shake device or press <ThemedText type="code">m</ThemedText> in terminal
      </ThemedText>
    );
  }
  const shortcut = Platform.OS === 'android' ? 'cmd+m (or ctrl+m)' : 'cmd+d';
  return (
    <ThemedText type="small">
      press <ThemedText type="code">{shortcut}</ThemedText>
    </ThemedText>
  );
}

export default function HomeScreen() {


   async function readData() {
      try {
        const { data } = await supabase.from('patients').select('*')
        console.log(data)
  
      } catch (error) {
        console.error(error);
      }
    }

    async function storeData(dateOfBirth: Date, sBP: number, dBP: number) {
      const { error } = await supabase.from('patients').insert({id: 2,
        created_at: new Date().toISOString(),
        dob: dateOfBirth.toISOString().split('T')[0],
        systolic_BP: [sBP],
        diastolic_BP: [dBP]
      })
      console.log(error)
    }

    const [dBP, setdBP] = React.useState('0');
    const [sBP, setsBP] = React.useState('0');


    const [date, setDate] = React.useState(new Date())
    const [open, setOpen] = React.useState(false)

  return (

    
    
    <ThemedView style={styles.container}>
      

      <SafeAreaView style={styles.safeArea}>
        <ThemedView style={styles.heroSection}>
          <AnimatedIcon />
          <ThemedText type="title" style={styles.title}>
            Welcome to&nbsp;Expo
          </ThemedText>
        </ThemedView>

        <ThemedText type="code" style={styles.code}>
          get started
        </ThemedText>

        <ThemedView type="backgroundElement" style={styles.stepContainer}>
          <HintRow
            title="Try editing"
            hint={<ThemedText type="code">src/app/index.tsx</ThemedText>}
          />
          <HintRow title="Dev tools" hint={getDevMenuHint()} />
          <HintRow
            title="Fresh start"
            hint={<ThemedText type="code">npm run reset-project</ThemedText>}
          />
        </ThemedView>

        <Button
        title='getData'
        onPress={() => {
        readData();
        }}
        />


        <TextInput
          onChangeText={setsBP}
          value={sBP}

        />

        <TextInput
          onChangeText={setdBP}
          value={dBP}

        />

        <Button title="Open" onPress={() => setOpen(true)} />
        {open && (
          <DateTimePicker
            value={date}
            mode="date"
            onChange={(event, selectedDate) => {
              setOpen(false);
              if (selectedDate) setDate(selectedDate);
            }}
          />
        )}

        <Button
        title='SUBMIT'
        onPress={() => {
          console.log(Intl.DateTimeFormat("en-GB").format(date))
          console.log(date)
          console.log(sBP)
          console.log(dBP)
          storeData(date, parseInt(sBP), parseInt(dBP));
        }}
        />
        

        {Platform.OS === 'web' && <WebBadge />}
      </SafeAreaView>
    </ThemedView>
    
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    flexDirection: 'row',
  },
  safeArea: {
    flex: 1,
    paddingHorizontal: Spacing.four,
    alignItems: 'center',
    gap: Spacing.three,
    paddingBottom: BottomTabInset + Spacing.three,
    maxWidth: MaxContentWidth,
  },
  heroSection: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    paddingHorizontal: Spacing.four,
    gap: Spacing.four,
  },
  title: {
    textAlign: 'center',
  },
  code: {
    textTransform: 'uppercase',
  },
  stepContainer: {
    gap: Spacing.three,
    alignSelf: 'stretch',
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.four,
    borderRadius: Spacing.four,
  },
});
