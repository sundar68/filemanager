export interface FileItem {
    id: string;
    name: string;
    type: string;
    size: number;
    url: string;
    uploadDate: Date;
  }

export interface FileState {
    files: FileItem[];
    loading: boolean;
    error: string | null;
    isUploading: boolean;
}

export type FileUploadBody = {
  name: string;
  type: string;
  size: number;
  file: File;
}

export const ALLOWED_TYPES = [
  'image/jpeg',
  'image/png',
  'text/plain',
  'application/json'
];
