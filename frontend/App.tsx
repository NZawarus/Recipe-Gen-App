import React, { Fragment, Component } from 'react';
import * as ImagePicker from "react-native-image-picker";
import CameraRoll from "@react-native-camera-roll/camera-roll";

import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
  Image,
  Button,
  Dimensions,
  TouchableOpacity,
  Platform,
  PermissionsAndroid,
  ActivityIndicator,
} from 'react-native';

export default class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      filePath: {
        data: '',
        uri: ''
      },
      fileData: '',
      fileUri: '',
      recipe: '',
      loading: false,
    }
  }

  handleImageForAPI = (imageUri) => {
    console.log('Image ready to send to API:', imageUri)
    // add logic to send image to API here
    this.fetchRecipe();
    }

  fetchRecipe = async () => {
    try {

      console.log('Fetching recipe from backend...');
      this.setState({ loading: true });

      // Simulate a backend response with a timeout (replace later with real API)
      setTimeout(() => {

        const fakeRecipe = `
        🍳 Quick Fridge Omelette Recipe:
        - 3 eggs
        - Leftover veggies (onions, bell peppers)
        - Cheese
        - Salt & pepper
        1. Whisk the eggs.
        2. Stir in chopped veggies and cheese.
        3. Cook on medium heat until set.
        Enjoy!
        `;

        this.setState({ recipeText: fakeRecipe.trim(),
                        loading: false });
        console.log('Recipe received and set.');

      }, 2000); // Simulate 2 seconds waiting time

      // When ready to connect to your real backend:
      /*
      const response = await fetch('https://your-backend-url.com/get-recipe');
      const data = await response.json();
      this.setState({ recipeText: data.recipe,
                      loading: false });
      */

    } catch (error) {

      console.error('Error fetching recipe:', error);
      this.setState({ loading: false });

    }
  }

  chooseImage = () => {
    let options = {
      title: 'Select Image',
      customButtons: [
        { name: 'customOptionKey', title: 'Choose Photo from Custom Option' },
      ],
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    ImagePicker.launchImageLibrary(options, (response) => {
      console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User canceled image picker by pressing back button');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User selected custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        const source = { uri: response.uri };

        // You can also display the image using data:
        // const source = { uri: 'data:image/jpeg;base64,' + response.data };
        // alert(JSON.stringify(response));s
        console.log('response', JSON.stringify(response));
        this.setState({
          filePath: response,
          fileData: response.data,
          fileUri: response.uri
        });
        this.handleImageForAPI(response.uri);
      }
    });
  }

  requestStoragePermission = async () => {
    if (Platform.OS === 'android') {
      if (Platform.Version >= 33) { // Android 13+
        const readGranted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.READ_MEDIA_IMAGES,
          {
            title: "Storage Permission",
            message: "App needs access to your photos to save pictures.",
            buttonNeutral: "Ask Me Later",
            buttonNegative: "Cancel",
            buttonPositive: "OK"
          }
        );
        return readGranted === PermissionsAndroid.RESULTS.GRANTED;
      } else { // Android 12 or lower
        const writeGranted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
          {
            title: "Storage Permission",
            message: "App needs access to your storage to save pictures.",
            buttonNeutral: "Ask Me Later",
            buttonNegative: "Cancel",
            buttonPositive: "OK"
          }
        );
        return writeGranted === PermissionsAndroid.RESULTS.GRANTED;
      }
    } else {
      return true; // iOS doesn't need explicit storage permission for CameraRoll
    }
  };


  launchCamera = async () => {
    try {
      const cameraGranted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.CAMERA,
        {
          title: "Camera Permission",
          message: "App needs camera permission to take photos.",
          buttonNeutral: "Ask Me Later",
          buttonNegative: "Cancel",
          buttonPositive: "OK"
        }
      );

      if (cameraGranted !== PermissionsAndroid.RESULTS.GRANTED) {
        console.log("Camera permission denied");
        return;
      }

      const options = {
        mediaType: 'photo',
        saveToPhotos: true,
        includeBase64: true,
      };

      ImagePicker.launchCamera(options, (response) => {
        console.log('Camera response:', response);

        if (response.didCancel) {
          console.log('User canceled camera');
        } else if (response.errorCode) {
          console.log('ImagePicker Error: ', response.errorMessage);
        } else if (response.assets && response.assets.length > 0) {
          const asset = response.assets[0];
          const tempUri = asset.uri;
          console.log('Captured image URI:', tempUri);

          this.setState({
            filePath: { uri: asset.uri, data: asset.base64 },
            fileData: asset.base64,
            fileUri: tempUri,
          });
          this.handleImageForAPI(asset.uri);
        }
      });
    } catch (err) {
      console.warn(err);
    }
  };



  renderFileData() {
    if (this.state.fileData) {
      return <Image source={{ uri: 'data:image/jpeg;base64,' + this.state.fileData }}
        style={styles.images}
      />
    } else {
      return <Image source={require('./assets/dummy.png')}
        style={styles.images}
      />
    }
  }

  renderFileUri() {
    if (this.state.fileUri) {
      return <Image
        source={{ uri: this.state.fileUri }}
        style={styles.images}
      />
    } else {
      return <Image
        source={require('./assets/galleryImages.jpg')}
        style={styles.images}
      />
    }
  }
  render() {
    return (
      <Fragment>
        <StatusBar barStyle="dark-content" />
        <SafeAreaView style={{flex: 1}}>
          <View style={styles.body}>
            <ScrollView contentContainerStyle={styles.scrollViewContent}>
              <Text style={{textAlign:'center',fontSize:20,paddingBottom:10}}>
                RecipeIQ Recipe Generator
              </Text>
              {this.state.loading ? (
                <View style={{padding: 20, alignItems: 'center'}}>
                  <ActivityIndicator size="large" color="#0000ff" />
                  <Text style={{marginTop: 10, fontSize: 16}}>Generating recipe...</Text>
                </View>
              ) : (
                this.state.recipeText ? (
                  <View style={{padding: 20}}>
                    <Text style={{fontSize: 18, fontWeight: 'bold', marginBottom: 10}}>Generated Recipe:</Text>
                    <Text style={{fontSize: 16}}>{this.state.recipeText}</Text>
                  </View>
                ) : null
              )}
            </ScrollView>

            {/* Buttons always on bottom */}
            <View style={styles.btnParentSection}>
              <TouchableOpacity onPress={this.chooseImage} style={styles.btnSection}  >
                <Text style={styles.btnText}>Choose File</Text>
              </TouchableOpacity>

              <TouchableOpacity onPress={this.launchCamera} style={styles.btnSection}  >
                <Text style={styles.btnText}>Launch Camera</Text>
              </TouchableOpacity>
            </View>

          </View>
        </SafeAreaView>
      </Fragment>
    );
  }
};

const colors = {
  white: '#FFFFFF',
  lighter: '#F3F3F3',
  black: '#000000',
  gray: '#D3D3D3',
  blue: '#0000FF',
};

const styles = StyleSheet.create({
  scrollView: {
    backgroundColor: colors.lighter,
  },

  body: {
    backgroundColor: colors.white,
    justifyContent: 'center',
    borderColor: 'black',
    borderWidth: 1,
    height: Dimensions.get('screen').height - 20,
    width: Dimensions.get('screen').width
  },
  ImageSections: {
    display: 'flex',
    flexDirection: 'row',
    paddingHorizontal: 8,
    paddingVertical: 8,
    justifyContent: 'center'
  },
  scrollViewContent: {
      flexGrow: 1,
      paddingBottom: 100,
  },
  images: {
    width: 150,
    height: 150,
    borderColor: 'black',
    borderWidth: 1,
    marginHorizontal: 3
  },
  btnParentSection: {
    position: 'absolute',
    bottom: 80,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center'
  },
  btnSection: {
    width: 150,
    height: 50,
    backgroundColor: '#DCDCDC',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 5
  },
  btnText: {
    textAlign: 'center',
    color: 'gray',
    fontSize: 14,
    fontWeight:'bold'
  }
});
