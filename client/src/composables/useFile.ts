const useFile = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];

    if (file) {
        const reader = new FileReader();
        
        return new Promise<{ file: File, fileDataURL: string | undefined }>((resolve) => {
            reader.onload = (e: ProgressEvent<FileReader>) => {
                if (e.target instanceof FileReader) {
                    const fileDataURL = e.target.result as string;
                    const fileData = {
                        file,
                        fileDataURL
                    }
                    resolve(fileData);
                } else {
                    resolve({ file, fileDataURL: undefined });
                }
            }
            reader.readAsDataURL(file)
        })
    }

    return Promise.resolve({ file: undefined, fileDataURL: undefined });
};

export default useFile;