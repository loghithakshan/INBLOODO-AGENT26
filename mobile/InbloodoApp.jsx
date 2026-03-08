import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Image,
  ActivityIndicator,
  Alert,
  StyleSheet,
  Dimensions,
} from 'react-native';
import DocumentPicker from 'react-native-document-picker';
import { Camera } from 'react-native-camera-roll';
import axios from 'axios';

const { width, height } = Dimensions.get('window');

export default function InbloodoApp() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const API_URL = 'https://impalpable-perspectively-andria.ngrok-free.dev';

  // Upload PDF
  const pickPDF = async () => {
    try {
      const doc = await DocumentPicker.pick({
        type: [DocumentPicker.types.pdf],
      });

      uploadFile(doc.uri, 'pdf');
    } catch (err) {
      if (!DocumentPicker.isCancel(err)) {
        Alert.alert('Error', 'Failed to pick PDF');
      }
    }
  };

  // Capture Image
  const captureImage = async () => {
    try {
      const photo = await Camera.launch({
        mediaType: 'photo',
      });

      if (photo) {
        uploadFile(photo.uri, 'image');
      }
    } catch (err) {
      Alert.alert('Error', 'Failed to capture image');
    }
  };

  // Upload File to API
  const uploadFile = async (uri, fileType) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', {
        uri,
        type: fileType === 'pdf' ? 'application/pdf' : 'image/jpeg',
        name: `report.${fileType === 'pdf' ? 'pdf' : 'jpg'}`,
      });

      const endpoint =
        fileType === 'pdf' ? '/analyze-pdf/' : '/analyze-image/';
      const response = await axios.post(`${API_URL}${endpoint}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
      setSelectedFile({ type: fileType, data: response.data });
      Alert.alert('Success', 'Analysis completed!');
    } catch (error) {
      Alert.alert('Error', 'Failed to analyze file: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Analyze JSON Data
  const analyzeJSON = async () => {
    // Sample data for demo
    const sampleData = {
      hemoglobin: 11.5,
      glucose: 180,
      cholesterol: 240,
      blood_pressure: 140,
      wbc: 7500,
      platelets: 250000,
      creatinine: 0.9,
      alt: 45,
      ast: 50,
      ldl: 160,
      hdl: 35,
    };

    setLoading(true);
    try {
      const response = await axios.post(
        `${API_URL}/analyze-report/`,
        sampleData
      );
      setResults(response.data);
      Alert.alert('Success', 'Analysis completed!');
    } catch (error) {
      Alert.alert('Error', 'Failed to analyze: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>🩺 INBLOODO</Text>
        <Text style={styles.subtitle}>AI Health Diagnostics</Text>
      </View>

      {/* Main Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Upload Blood Report</Text>

        <TouchableOpacity
          style={[styles.button, styles.primaryButton]}
          onPress={pickPDF}
          disabled={loading}
        >
          <Text style={styles.buttonText}>📄 Upload PDF</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={captureImage}
          disabled={loading}
        >
          <Text style={styles.buttonText}>📸 Capture Image</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.tertiaryButton]}
          onPress={analyzeJSON}
          disabled={loading}
        >
          <Text style={styles.buttonText}>📊 Sample Analysis</Text>
        </TouchableOpacity>
      </View>

      {/* Loading */}
      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#1f4788" />
          <Text style={styles.loadingText}>Analyzing...</Text>
        </View>
      )}

      {/* Results */}
      {results && !loading && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>📋 Analysis Results</Text>

          {/* Parameters */}
          {results.extracted_parameters && (
            <View style={styles.resultSection}>
              <Text style={styles.resultSubtitle}>Blood Parameters</Text>
              {Object.entries(results.extracted_parameters).map(
                ([key, value]) => (
                  <View key={key} style={styles.parameterRow}>
                    <Text style={styles.parameterName}>{key}:</Text>
                    <Text style={styles.parameterValue}>{value}</Text>
                  </View>
                )
              )}
            </View>
          )}

          {/* Risks */}
          {results.risks && results.risks.length > 0 && (
            <View style={styles.resultSection}>
              <Text style={styles.resultSubtitle}>⚠️ Identified Risks</Text>
              {results.risks.map((risk, index) => (
                <Text key={index} style={styles.riskText}>
                  • {risk}
                </Text>
              ))}
            </View>
          )}

          {/* Recommendations */}
          {results.recommendations && results.recommendations.length > 0 && (
            <View style={styles.resultSection}>
              <Text style={styles.resultSubtitle}>💡 Recommendations</Text>
              {results.recommendations.map((rec, index) => (
                <Text key={index} style={styles.recommendationText}>
                  {index + 1}. {rec}
                </Text>
              ))}
            </View>
          )}

          {/* Download Button */}
          {results.pdf_report && (
            <TouchableOpacity style={styles.downloadButton}>
              <Text style={styles.buttonText}>📥 Download Full Report</Text>
            </TouchableOpacity>
          )}
        </View>
      )}

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          ⚠️ For educational purposes only.
          {'\n'}Not a substitute for professional medical advice.
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: '#1f4788',
    paddingVertical: 30,
    paddingHorizontal: 20,
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#e0e0e0',
  },
  section: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 15,
    color: '#333',
  },
  button: {
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginBottom: 10,
    alignItems: 'center',
  },
  primaryButton: {
    backgroundColor: '#1f4788',
  },
  secondaryButton: {
    backgroundColor: '#3b6aa0',
  },
  tertiaryButton: {
    backgroundColor: '#5a8cc8',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  loadingContainer: {
    paddingVertical: 40,
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  resultsContainer: {
    backgroundColor: '#fff',
    marginHorizontal: 20,
    borderRadius: 8,
    padding: 20,
    marginBottom: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#1f4788',
  },
  resultSection: {
    marginBottom: 20,
    paddingBottom: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  resultSubtitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 10,
  },
  parameterRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 5,
  },
  parameterName: {
    flex: 1,
    color: '#666',
    fontSize: 14,
  },
  parameterValue: {
    fontWeight: '600',
    color: '#1f4788',
    fontSize: 14,
  },
  riskText: {
    color: '#d32f2f',
    fontSize: 14,
    marginBottom: 8,
    lineHeight: 20,
  },
  recommendationText: {
    color: '#388e3c',
    fontSize: 14,
    marginBottom: 8,
    lineHeight: 20,
  },
  downloadButton: {
    backgroundColor: '#388e3c',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 6,
    alignItems: 'center',
    marginTop: 15,
  },
  footer: {
    paddingHorizontal: 20,
    paddingVertical: 30,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
    lineHeight: 18,
  },
});
