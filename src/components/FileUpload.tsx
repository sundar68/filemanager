import React, { useRef } from 'react';
import { UploadCloud } from 'lucide-react';
import styles from './FileUpload.module.css';
import { ALLOWED_TYPES } from '../types/fileType';
import { useFiles } from '../hooks/useFile';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
}


const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {

  // const {uploadFileAction, isUploading} = useFiles();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!ALLOWED_TYPES.includes(file.type)) {
      alert('Unsupported file type. Please upload JPG, PNG, TXT, or JSON files.');
      return;
    }

    onFileUpload(file);
    console.log(file.name, file.type, file.size);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className={styles.uploadContainer}>
      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
        accept={ALLOWED_TYPES.join(',')}
        className={styles.fileInput}
        id="fileInput"
      />
      <label htmlFor="fileInput" className={styles.uploadButton}>
        <UploadCloud className={styles.uploadIcon} />
        <span>Upload File</span>
      </label>
    </div>
  );
};

export default FileUpload;