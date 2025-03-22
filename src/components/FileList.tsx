import React from 'react';
import { FileIcon, ImageIcon, FileTextIcon } from 'lucide-react';
import { Link } from 'react-router-dom';
import { FileItem } from '../types/fileType';
import styles from './FileList.module.css';

interface FileListProps {
  files: FileItem[];
}

const FileList: React.FC<FileListProps> = ({ files = [] }) => {
  
  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return <ImageIcon />;
    if (type === 'text/plain') return <FileTextIcon />;
    return <FileIcon />;
  };

  return (
    <div className={styles.fileList}>
      {files && files.map((file) => (
        <Link to={`/view/${file.id}`} key={file.id} className={styles.fileItem}>
          <div className={styles.fileIcon}>{getFileIcon(file.type)}</div>
          <div className={styles.fileInfo}>
            <span className={styles.fileName}>{file.name}</span>
            <span className={styles.fileSize}>
              {(file.size / 1024).toFixed(2)} KB
            </span>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default FileList;