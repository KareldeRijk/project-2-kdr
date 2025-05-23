import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { classifyImage } from './axios'

interface Prediction {
  class: string;
  confidence: number;
}

function App() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setErorr] = useState(false)
  const [predictions, setPredictions] = useState<Prediction[]>([]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setErorr(false)
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const reader = new FileReader();

      reader.onabort = () => console.log('file reading was aborted');
      reader.onerror = () => console.log('file reading has failed');
      reader.onload = async () => {
        const base64Image = reader.result as string;
        const base64Data = base64Image.split(',')[1];
        setSelectedImage(base64Image);
        setIsLoading(true);
        try {
          const result = await classifyImage(base64Data);
          console.log(result)
          setPredictions(result.predictions);
        } catch (error) {
          setErorr(true)
          console.error('Fehler bei der Bildklassifizierung:', error);
        } finally {
          setIsLoading(false);
        }
      };
      reader.readAsDataURL(file);
    }
  }, []);
  
  const {getRootProps, getInputProps} = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxFiles: 1
  })

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <div className="bg-white p-8 pb-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Image class predictions</h1>
        <p className="text-red">Our pre-trained model <b>DenseNet201</b> is able to predict 10 classes:</p>
        <b>airplanes, automobiles, birds, cats, deers, dogs, frogs, horses, ships and trucks</b>

        <div className="w-full  mx-auto mt-8 mb-8">
          {selectedImage ? (
            <div 
              {...getRootProps()} 
              className="relative aspect-[4/3] w-full cursor-pointer"
            >
              <input {...getInputProps()} />
              <img 
                src={selectedImage} 
                alt="Vorschau" 
                className="w-full h-full object-cover rounded-lg shadow-md"
              />
            </div>
          ) : (
            <div 
              {...getRootProps()} 
              className='border-2 border-dashed border-gray-300 rounded-lg p-8 aspect-[4/3] w-full cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors duration-200 ease-in-out flex items-center justify-center'
            >
              <input {...getInputProps()} />
              <div className='flex flex-col items-center justify-center text-gray-600'>
                <svg className="w-12 h-12 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
                <p className="text-lg font-medium">Drag image here</p>
                <p className="text-sm mt-1">or click to select</p>
                <p className="text-xs mt-2 text-gray-500">Only JPG and PNG files allowed</p>
              </div>
            </div>
          )}
        </div>
        <div className='flex justify-between' style={{height: 24}}>
          {error && (<p>An error has occurred!</p>)}
          {isLoading && (<i>Loading the results...</i>)}
          {!error && !isLoading && predictions.map(pred => (
            <b>
              {pred.class.charAt(0).toUpperCase() + pred.class.slice(1)}: {(pred.confidence * 100).toFixed(1)}%
            </b>
          ))}
        </div>
      </div>      
    </div>
  )
}

export default App
