from flask import Flask, render_template, jsonify, request
# from ortools.constraint_solver import routing_enums_pb2  # <-- GEÇİCİ OLARAK KAPATILDI
# from ortools.constraint_solver import pywrapcp  # <-- GEÇİCİ OLARAK KAPATILDI
import os

app = Flask(__name__)

# --- 1. Master Data (Our "Database") ---
# Bu veride bir değişiklik yok
MASTER_LOCATION_DATA = {
    'Depot (Giriş)': [37.7744, 29.0929],  # Denizli center
    'Adres A': [37.7795, 29.0950],  # Near Pamukkale Univ. Hospital
    'Adres B': [37.7818, 29.0838],  # Near Servergazi
    'Adres C': [37.7681, 29.0886],  # Near Bus Station (Otogar)
    'Adres D': [37.7750, 29.1050]  # Near Çamlık
}
MASTER_LOCATION_NAMES = list(MASTER_LOCATION_DATA.keys())

MASTER_DISTANCE_MATRIX = [
    [0, 548, 776, 696, 582],  # Depot (0)
    [548, 0, 684, 801, 864],  # Adres A (1)
    [776, 684, 0, 992, 114],  # Adres B (2)
    [696, 801, 992, 0, 794],  # Adres C (3)
    [582, 864, 114, 794, 0],  # Adres D (4)
]


# --- 2. Dynamic Data Model Builder (Bu fonksiyona artık ihtiyaç yok) ---
# def create_dynamic_data_model(selected_location_names):
#    ... (Tüm bu fonksiyonu silebiliriz ama şimdilik kalsın)


# --- 3. The Routes ---
@app.route('/')
def home():
    """
    Renders the main HTML page.
    """
    address_names = [name for name in MASTER_LOCATION_NAMES if name != 'Depot (Giriş)']
    return render_template('index.html', address_names=address_names)


@app.route('/solve', methods=['POST'])
def solve():
    """
    BU ŞİMDİ SADECE SAHTE (DUMMY) BİR FONKSİYON
    """
    try:
        post_data = request.get_json()
        selected_names_from_user = post_data['locations']

        # Seçilen isimleri al
        locations_for_solver = ['Depot (Giriş)'] + selected_names_from_user

        # Sahte veriyi oluştur
        fake_route_result = []
        for name in locations_for_solver:
            if name in MASTER_LOCATION_DATA:
                fake_route_result.append({
                    'name': name,
                    'coords': MASTER_LOCATION_DATA[name]
                })

        # Depoyu sona ekle
        fake_route_result.append({
            'name': 'Depot (Giriş)',
            'coords': MASTER_LOCATION_DATA['Depot (Giriş)']
        })

        # Optimizasyon yapmadan, sahte rotayı direkt gönder
        return jsonify({'status': 'success', 'route': fake_route_result})

        # --- ORTOOLS KODUNUN TAMAMI DEVRE DIŞI ---

    except Exception as e:
        print(e)  # Log the error to the console
        return jsonify({'status': 'error', 'message': 'Hatalı veri. Lütfen en az bir adres seçin.'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)