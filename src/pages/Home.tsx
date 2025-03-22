import React, { useState, useEffect } from 'react';
import FileList from '../components/FileList';
import FileUpload from '../components/FileUpload';
import { FileItem } from '../types/fileType';
import styles from './Home.module.css';
import { useFiles } from '../hooks/useFile';

const Home: React.FC = () => {
  const { files, fileLoading, fileError, getFiles, uploadFileAction } = useFiles();
  // const [files, setFiles] = useState<FileItem[]>([]);

  useEffect(() => {
    getFiles();
  }, []);

  const handleFileUpload = (file: File) => {
    const newFile: FileItem = {
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      type: file.type,
      size: file.size,
      url: URL.createObjectURL(file),
      uploadDate: new Date()
    };
    console.log(newFile);
    uploadFileAction({ name: file.name, type: file.type, size: file.size, file });
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Files</h1>
      <FileUpload onFileUpload={handleFileUpload} />
      <FileList files={files} />
    </div>
  );
};

export default Home;