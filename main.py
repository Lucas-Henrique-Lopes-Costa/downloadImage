import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import quote_plus

class SimpleImageDownloader:
    def __init__(self, save_folder="downloaded_images"):
        """
        Inicializa o downloader de imagens
        :param save_folder: Pasta onde as imagens serão salvas
        """
        self.save_folder = save_folder
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
            
        # Headers para simular um navegador
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def download_images(self, search_term, num_images=10):
        """
        Baixa imagens do Bing Images
        :param search_term: Termo para pesquisar
        :param num_images: Número de imagens para baixar
        """
        # Criar pasta específica para o termo de busca
        search_folder = os.path.join(self.save_folder, search_term.replace(" ", "_"))
        if not os.path.exists(search_folder):
            os.makedirs(search_folder)

        # URL do Bing Images
        encoded_search = quote_plus(search_term)
        url = f"https://www.bing.com/images/search?q={encoded_search}&form=HDRSC2&first=1"

        try:
            # Fazer a requisição
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontrar links de imagens
            images = soup.find_all('a', class_='iusc')
            downloaded = 0
            
            for img in images:
                if downloaded >= num_images:
                    break
                    
                try:
                    # Extrair URL da imagem
                    img_data = eval(img.get('m', '{}'))
                    img_url = img_data.get('murl', '')
                    
                    if img_url:
                        # Baixar a imagem
                        img_response = requests.get(img_url, headers=self.headers, timeout=10)
                        
                        if img_response.status_code == 200:
                            # Determinar extensão do arquivo
                            content_type = img_response.headers.get('content-type', '')
                            ext = self._get_extension(content_type)
                            
                            # Salvar imagem
                            file_name = f"image_{downloaded + 1}{ext}"
                            file_path = os.path.join(search_folder, file_name)
                            
                            with open(file_path, 'wb') as f:
                                f.write(img_response.content)
                            
                            downloaded += 1
                            print(f"Baixada imagem {downloaded} de {num_images} para '{search_term}'")
                            
                            # Pequena pausa para evitar sobrecarga
                            time.sleep(1)
                            
                except Exception as e:
                    print(f"Erro ao baixar imagem: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Erro na busca: {str(e)}")

    def _get_extension(self, content_type):
        """
        Determina a extensão do arquivo baseado no content-type
        """
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        return '.jpg'  # default

# Exemplo de uso
if __name__ == "__main__":
    downloader = SimpleImageDownloader()
    
    # Lista de termos para buscar do arquivo keywords.txt
    search_terms = []

    with open("keywords.txt", "r") as f:
        for line in f:
            search_terms.append(line.strip())
    
    # Baixar imagens para cada termo
    for term in search_terms:
        print(f"\nIniciando download para: {term}")
        downloader.download_images(term, num_images=10)
        print(f"Concluído: {term}")