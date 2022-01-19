import requests
class scanner:
    def __init__(self, nama_input_file, nama_output_file):
        print("Scanner Versi Wordpress, melakukan inisialisasi data")
        self.header={
            "referer": "https://www.google.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
            }
        self.not_found="NOT FOUND"
        self.nama_input_file=nama_input_file
        self.nama_output_file=nama_output_file
        self.counter_url=1
        self.inisialisasi_input_file()
        self.counter_found=0
        self.counter_not_found=0
        self.versi=-1
        self.is_process_stop=False
        print("File Masukan : " + self.nama_input_file)
        print("File Keluaran : " + self.nama_output_file)
        print("Percobaan dilakukan pada "+str(len(self.list_url)) + " File")
        
    def format_url(self):
        if self.current_url[-1]=='/':
            self.current_url=self.current_url[:-1]
        urlsub=self.current_url.split("//")
        if len(urlsub)==1:
            self.current_url="https://"+self.current_url

    def main(self):
        for url in self.list_url:
            self.versi=-1
            self.is_process_stop=False
            self.current_url=url.replace("\n","")
            self.format_url()
            self.process_single_url()
        print("Proses Selesai")
        print("ditemukan "+str(self.counter_found) + " versi Wordpress")
        print("Tidak ditemukan "+str(self.counter_not_found) + " versi Wordpress")

    def inisialisasi_input_file(self):
        self.list_url=open(self.nama_input_file,"r").readlines()

    def buka_file_out(self):
        self.file_out=open(self.nama_output_file,"a")

    def tutup_file_out(self):
        self.file_out.close()

    def tulis_file_out(self,yang_ditulis):
        self.buka_file_out()
        self.file_out.write(yang_ditulis+"\n")
        self.tutup_file_out()

    def set_header(self,header):
        self.header=header

    def process_single_url(self):
        print("\nProcessing "+str(self.counter_url)+"/"+str(len(self.list_url)) +" - "+self.current_url)    
        urlsub=self.current_url.split("//")
        urlsplit=urlsub[1].split("/")
        prefix=urlsub[0]+"//"
        feed="/feed"
        base=urlsplit[0]
        for i in urlsplit:
            if self.is_process_stop:
                break
            if base != i:
                base=base+"/"+i
            try:
                processing_url=prefix+base+feed
                print("Try Request to "+processing_url)
                re=requests.get(processing_url,headers=self.header)
                text=re.text
                self.cariversi(text)
                if self.versi != -1:
                    self.tulis_file_out(str(self.counter_url)+";"+self.current_url+";"+self.versi)
                    self.counter_url+=1
                    self.counter_found+=1
                    break
            except requests.exceptions.ConnectionError:
                print("Exception: Website "+self.current_url+" tidak bisa diakses")
                self.is_process_stop=True
            except Exception as e:
                self.error_handling(e)
        if self.versi == -1:
            self.tulis_file_out(str(self.counter_url)+";"+self.current_url+";"+self.not_found)
            self.counter_not_found+=1
            self.counter_url+=1
            pass
    def error_handling(self,e):
        print("Exception: "e,self.current_url)

    def cariversi(self, text):
        cari1=text.find("<generator>")
        if cari1==-1:
            self.versi=cari1
        else:
            cari2=text.find("</generator>")
            wp= text[cari1+11:cari2]
            versi=wp.split("?v=")[1]
            self.versi=versi