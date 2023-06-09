import os
import subprocess, time,socket, sys
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image


def validate_path():
    while True:
        try:
            path = input("Por favor, ingrese la ruta de la carpeta a procesar (o 'q' para salir): ")
            path = Path(path).resolve()
            if path == Path('q').resolve():
                return None
            elif not path.exists():
                print("La ruta ingresada no existe.")
            elif not path.is_dir():
                print("La ruta ingresada no es una carpeta válida.")
            else:
                return path
        except Exception as e:
            print(f"Ocurrió un error: {e}")


def count_files(folder_path):
    file_count = {}
    for filepath in folder_path.glob('*'):
        if filepath.is_file():
            ext = filepath.suffix[1:].lower()
            if ext in file_count:
                file_count[ext] += 1
            else:
                file_count[ext] = 1
    return file_count


def convert_images(output_format='webp'):
    folder_path = validate_path()
    if folder_path is None:
        return
    delete_originals = input("Desea eliminar los archivos originales? [S/N]: ")
    while delete_originals.lower() not in ['s', 'n']:
        print('Opción inválida. Por favor, ingrese "S" o "N".')
        delete_originals = input("Desea eliminar los archivos originales? [S/N]: ")
    file_count = count_files(folder_path)
    total_imgs = file_count.get(output_format, 0)
    converted_imgs = 0
    failed_imgs = 0
    original_imgs = 0
    skipped_imgs = 0

    for filepath in folder_path.glob('*'):
        if filepath.is_file() and filepath.suffix[1:].lower() == output_format:
            original_imgs += 1
            continue
        elif filepath.is_file() and filepath.suffix[1:].lower() in file_count:
            if filepath.suffix[1:].lower() == 'webp':
                skipped_imgs += 1
                continue
            output_path = filepath.with_suffix(f'.{output_format}')
            try:
                with Image.open(filepath) as img:
                    img.save(output_path, output_format)
                    converted_imgs += 1
                    # print(f'{filepath} -> {output_path}')
                    if delete_originals.lower() == 's':
                        os.remove(filepath)
                        # print(f'{filepath} eliminado.')
            except Exception as e:
                print(f"No se pudo convertir la imagen {filepath}: {e}")
                failed_imgs += 1

    remaining_files = count_files(folder_path)
    remaining_wepb = remaining_files.get(output_format, 0)
    total_wepb = converted_imgs + total_imgs

    print(f"Total de imágenes: {sum(file_count.values())}")
    print(f"Cantidad de imágenes por tipo: {file_count}")
    print(f"Imágenes convertidas correctamente: {converted_imgs}")
    print(f"Imágenes no convertidas: {failed_imgs}")
    print(f"Imágenes originales conservadas: {original_imgs}")
    print(f"Imágenes en formato {output_format} ya existentes: {total_imgs}")
    print(f"Imágenes {output_format} eliminadas: {converted_imgs if delete_originals.lower() == 's' else 0}")
    print(f"Imágenes restantes en formato {output_format}: {remaining_wepb}")
    print(f"Imágenes restantes en otros formatos: {sum(remaining_files.values()) - remaining_wepb}")
    print(f"Total de imágenes en formato {output_format}: {total_wepb}")


def count_videos(folder_path):
    video_count = {}
    for filepath in folder_path.glob('*'):
        if filepath.is_file() and filepath.suffix[1:].lower() in ["mp4", "avi", "mov", "mkv", "webm"]:
            video_count[filepath.suffix[1:].lower()] = video_count.get(filepath.suffix[1:].lower(), 0) + 1
    return video_count


def convert_videos(output_format='webm'):
    folder_path = validate_path()
    if folder_path is None:
        return
    delete_originals = input("Desea eliminar los archivos originales? [S/N]: ")
    while delete_originals.lower() not in ['s', 'n']:
        print('Opción inválida. Por favor, ingrese "S" o "N".')
        delete_originals = input("Desea eliminar los archivos originales? [S/N]: ")
    video_count = count_videos(folder_path)
    total_vids = video_count.get(output_format, 0)
    converted_vids = 0
    failed_vids = 0
    original_vids = 0
    skipped_vids = 0

    for filepath in folder_path.glob('*'):
        if filepath.is_file() and filepath.suffix[1:].lower() == output_format:
            original_vids += 1
            continue
        elif filepath.is_file() and filepath.suffix[1:].lower() in ["mp4", "avi", "mov", "mkv"]:
            if filepath.suffix[1:].lower() == output_format:
                skipped_vids += 1
                continue
            output_path = filepath.with_suffix(f'.{output_format}')
            try:
                video = VideoFileClip(str(filepath))
                video.write_videofile(str(output_path))
                converted_vids += 1
                # print(f'{filepath} -> {output_path}')
                if delete_originals.lower() == 's':
                    os.remove(filepath)
                    # print(f'{filepath} eliminado.')
            except Exception as e:
                print(f"No se pudo convertir el video {filepath}: {e}")
                failed_vids += 1
                continue

    remaining_vids = count_videos(folder_path).get(output_format, 0)
    total_webm = converted_vids + total_vids

    print(f"Total de videos: {sum(video_count.values())}")
    print(f"Cantidad de videos por tipo: {video_count}")
    print(f"Videos convertidos correctamente: {converted_vids}")
    print(f"Videos no convertidos: {failed_vids}")
    print(f"Videos originales conservados: {original_vids}")
    print(f"Videos en formato {output_format} ya existentes: {total_vids}")
    print(f"Videos {output_format} eliminados: {converted_vids if delete_originals.lower() == 's' else 0}")
    print(f"Videos restantes en formato {output_format}: {remaining_vids}")
    print(f"Videos restantes en otros formatos: {sum(count_videos(folder_path).values()) - remaining_vids}")
    print(f"Total de videos en formato {output_format}: {total_webm}")


def install_module(module_name):
    try:
        subprocess.run(['pip', 'install', module_name], check=True)
        print(f"{module_name} instalado exitosamente.")
    except subprocess.CalledProcessError:
        print(f"No se pudo instalar {module_name}.")

def install_required_modules():
    modules = ['','pathlib', 'moviepy', 'Pillow']
    for module in modules:
        install_module(module)

def convert_media():
    print('Esta versión aún no cuenta con esta función')
    time.sleep(2)  # Espera 2 segundos
    return  # Retorna al menú principal


def good_bye():
    hostname = socket.gethostname()
    
    team_name = ("RALLENDE")
    print(f"Hasta luego! Gracias por usar la aplicación en {hostname}.\n desde el equipo {team_name}!")

    # Imprimir un gato
    print(r"""
 /\_/\  
( o   o )
=(  =  )=
  )   ( 
 (__ __)
""")
    time.sleep(2) # esperar 2 segundos antes de salir del programa
    sys.exit()


def print_menu():
    print("")
    print("Seleccione una opción:")
    print("0 - instalar modulos Faltantes")
    print("1 - Convertir imágenes a WebP")
    print("2 - Convertir videos a WebM")
    print("3 - Convertir ambos")
    print("4 - Salir")
    print("")


def main():
    print("")
    print("Bienvenido al conversor de archivos.")
    print("By Rallende.")
    print("")
    while True:
        print_menu()
        opcion = input()
        if opcion == '0':
            install_required_modules()
        elif opcion == '1':
            convert_images()
        elif opcion == '2':
            convert_videos()      
        elif opcion == '3':
            convert_media()      
        elif opcion == '4':
            good_bye()      
        else:
            print("")
            print("Opción no válida. Intente de nuevo.")
            print("")


if __name__ == "__main__":
    main()