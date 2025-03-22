import axios from 'axios';
import { FileUploadBody } from '../types/fileType';


const api = axios.create({
  baseURL: 'http://localhost:3210',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

export const filesApi = {
    getFiles: async () => {
        try {
            const response = await api.get('/files');
            return response.data;
        } catch (error) {
            console.error('Error fetching files:', error);
            throw error;
        }
    },
    uploadFile: async (body: FileUploadBody) => {
        const formData = new FormData();
        formData.append('file', body.file);

        const response = await api.post(`/files/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'accept': 'application/json',
            },
            params: {
                name: body.name,
                type: body.type,
                size: body.size,
            },
        });
        return response;
    },
};