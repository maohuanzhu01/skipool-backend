"""
Management command per popolare il database con le principali piste da sci italiane e dintorni.
Esegui con: python manage.py populate_ski_resorts
"""

from django.core.management.base import BaseCommand
from rides.models import SkiResort


SKI_RESORTS_DATA = [
    # LOMBARDIA
    {
        "name": "Piani di Bobbio - Valsassina",
        "alternative_names": "Bobbio, Piani Bobbio, Valsassina Ski, Barzio",
        "region": "lombardia",
        "province": "Lecco",
        "lat": 45.9617,
        "lng": 9.4533,
        "altitude_min": 1080,
        "altitude_max": 1700,
        "km_slopes": 35,
        "lifts_count": 14,
        "website": "https://www.pianidibobbio.com"
    },
    {
        "name": "Montecampione",
        "alternative_names": "Monte Campione, Campione, Plan di Montecampione",
        "region": "lombardia",
        "province": "Brescia",
        "lat": 45.8867,
        "lng": 10.2783,
        "altitude_min": 1200,
        "altitude_max": 2000,
        "km_slopes": 30,
        "lifts_count": 9,
        "website": "https://www.montecampione.eu"
    },
    {
        "name": "Aprica",
        "alternative_names": "Aprica Ski, Magnolta, Baradello",
        "region": "lombardia",
        "province": "Sondrio",
        "lat": 46.1533,
        "lng": 10.1517,
        "altitude_min": 1162,
        "altitude_max": 2300,
        "km_slopes": 50,
        "lifts_count": 12,
        "website": "https://www.apricaonline.com"
    },
    {
        "name": "Bormio",
        "alternative_names": "Bormio Ski, Bormio 2000, Bormio 3000, Cima Bianca, Valdisotto",
        "region": "lombardia",
        "province": "Sondrio",
        "lat": 46.4683,
        "lng": 10.3700,
        "altitude_min": 1225,
        "altitude_max": 3012,
        "km_slopes": 50,
        "lifts_count": 14,
        "website": "https://www.bormioski.eu"
    },
    {
        "name": "Livigno",
        "alternative_names": "Livigno Ski, Carosello 3000, Mottolino, Costaccia, Piccolo Tibet",
        "region": "lombardia",
        "province": "Sondrio",
        "lat": 46.5383,
        "lng": 10.1350,
        "altitude_min": 1816,
        "altitude_max": 2798,
        "km_slopes": 115,
        "lifts_count": 31,
        "website": "https://www.livigno.eu"
    },
    {
        "name": "Santa Caterina Valfurva",
        "alternative_names": "Santa Caterina, Valfurva, S. Caterina",
        "region": "lombardia",
        "province": "Sondrio",
        "lat": 46.4083,
        "lng": 10.5000,
        "altitude_min": 1738,
        "altitude_max": 2800,
        "km_slopes": 35,
        "lifts_count": 9,
        "website": "https://www.santacaterina.it"
    },
    {
        "name": "Madesimo - Valchiavenna",
        "alternative_names": "Madesimo, Valchiavenna, Madesimo Ski, Campodolcino",
        "region": "lombardia",
        "province": "Sondrio",
        "lat": 46.4317,
        "lng": 9.3517,
        "altitude_min": 1550,
        "altitude_max": 2948,
        "km_slopes": 60,
        "lifts_count": 14,
        "website": "https://www.skiareavalchiavenna.it"
    },
    {
        "name": "Chiesa in Valmalenco",
        "alternative_names": "Valmalenco, Chiesa Valmalenco, Palù, Alpe Palù, Snow Eagle",
        "region": "lombardia",
        "province": "Sondrio",
        "lat": 46.2633,
        "lng": 9.8500,
        "altitude_min": 1000,
        "altitude_max": 2336,
        "km_slopes": 60,
        "lifts_count": 12,
        "website": "https://www.valmalenco.eu"
    },
    {
        "name": "Ponte di Legno - Tonale",
        "alternative_names": "Ponte di Legno, Tonale, Passo Tonale, Adamello Ski, Presena",
        "region": "lombardia",
        "province": "Brescia",
        "lat": 46.2583,
        "lng": 10.5083,
        "altitude_min": 1121,
        "altitude_max": 3016,
        "km_slopes": 100,
        "lifts_count": 28,
        "website": "https://www.adamelloski.com"
    },
    {
        "name": "Foppolo - Carona",
        "alternative_names": "Foppolo, Carona, Brembo Ski, San Simone",
        "region": "lombardia",
        "province": "Bergamo",
        "lat": 46.0433,
        "lng": 9.7533,
        "altitude_min": 1508,
        "altitude_max": 2200,
        "km_slopes": 30,
        "lifts_count": 10,
        "website": "https://www.brembo-ski.eu"
    },
    {
        "name": "Presolana Monte Pora",
        "alternative_names": "Presolana, Monte Pora, Pora, Castione della Presolana",
        "region": "lombardia",
        "province": "Bergamo",
        "lat": 45.9150,
        "lng": 10.0617,
        "altitude_min": 1280,
        "altitude_max": 1880,
        "km_slopes": 30,
        "lifts_count": 11,
        "website": "https://www.presolana.it"
    },
    
    # TRENTINO-ALTO ADIGE
    {
        "name": "Madonna di Campiglio",
        "alternative_names": "Campiglio, Madonna Campiglio, Skirama Dolomiti, Pinzolo",
        "region": "trentino",
        "province": "Trento",
        "lat": 46.2283,
        "lng": 10.8267,
        "altitude_min": 850,
        "altitude_max": 2504,
        "km_slopes": 150,
        "lifts_count": 57,
        "website": "https://www.campigliodolomiti.it"
    },
    {
        "name": "Val di Fassa",
        "alternative_names": "Fassa, Canazei, Campitello, Moena, Pozza, Dolomiti Superski, Belvedere",
        "region": "trentino",
        "province": "Trento",
        "lat": 46.4767,
        "lng": 11.7700,
        "altitude_min": 1224,
        "altitude_max": 3269,
        "km_slopes": 210,
        "lifts_count": 80,
        "website": "https://www.fassa.com"
    },
    {
        "name": "Val Gardena",
        "alternative_names": "Gardena, Ortisei, Selva, S. Cristina, Santa Cristina, Seceda, Dolomiti Superski",
        "region": "trentino",
        "province": "Bolzano",
        "lat": 46.5567,
        "lng": 11.7650,
        "altitude_min": 1236,
        "altitude_max": 2518,
        "km_slopes": 175,
        "lifts_count": 79,
        "website": "https://www.valgardena.it"
    },
    {
        "name": "Alta Badia",
        "alternative_names": "Badia, Corvara, Colfosco, La Villa, San Cassiano, Dolomiti Superski",
        "region": "trentino",
        "province": "Bolzano",
        "lat": 46.5450,
        "lng": 11.8683,
        "altitude_min": 1324,
        "altitude_max": 2778,
        "km_slopes": 130,
        "lifts_count": 53,
        "website": "https://www.altabadia.org"
    },
    {
        "name": "Plan de Corones - Kronplatz",
        "alternative_names": "Plan de Corones, Kronplatz, Brunico, San Vigilio, Valdaora, Riscone",
        "region": "trentino",
        "province": "Bolzano",
        "lat": 46.7383,
        "lng": 11.9583,
        "altitude_min": 973,
        "altitude_max": 2275,
        "km_slopes": 119,
        "lifts_count": 32,
        "website": "https://www.kronplatz.com"
    },
    {
        "name": "Alpe di Siusi",
        "alternative_names": "Seiser Alm, Siusi, Castelrotto, Compaccio",
        "region": "trentino",
        "province": "Bolzano",
        "lat": 46.5417,
        "lng": 11.6217,
        "altitude_min": 1850,
        "altitude_max": 2350,
        "km_slopes": 60,
        "lifts_count": 22,
        "website": "https://www.seiseralm.it"
    },
    {
        "name": "San Martino di Castrozza - Passo Rolle",
        "alternative_names": "San Martino, Castrozza, Passo Rolle, Rolle, Pale di San Martino",
        "region": "trentino",
        "province": "Trento",
        "lat": 46.2617,
        "lng": 11.8017,
        "altitude_min": 1404,
        "altitude_max": 2357,
        "km_slopes": 60,
        "lifts_count": 26,
        "website": "https://www.sanmartino.com"
    },
    {
        "name": "Folgarida - Marilleva",
        "alternative_names": "Folgarida, Marilleva, Val di Sole, Skirama",
        "region": "trentino",
        "province": "Trento",
        "lat": 46.2933,
        "lng": 10.8550,
        "altitude_min": 1300,
        "altitude_max": 2180,
        "km_slopes": 60,
        "lifts_count": 22,
        "website": "https://www.valdisole.net"
    },
    {
        "name": "Andalo - Fai della Paganella",
        "alternative_names": "Andalo, Paganella, Fai della Paganella, Molveno",
        "region": "trentino",
        "province": "Trento",
        "lat": 46.1617,
        "lng": 11.0033,
        "altitude_min": 1042,
        "altitude_max": 2125,
        "km_slopes": 50,
        "lifts_count": 11,
        "website": "https://www.paganella.net"
    },
    
    # PIEMONTE
    {
        "name": "Sestriere",
        "alternative_names": "Sestrière, Via Lattea, Vialattea",
        "region": "piemonte",
        "province": "Torino",
        "lat": 44.9567,
        "lng": 6.8783,
        "altitude_min": 1350,
        "altitude_max": 2823,
        "km_slopes": 400,
        "lifts_count": 70,
        "website": "https://www.vialattea.it"
    },
    {
        "name": "Bardonecchia",
        "alternative_names": "Bardonecchia Ski, Jafferau, Colomion, Campo Smith",
        "region": "piemonte",
        "province": "Torino",
        "lat": 45.0783,
        "lng": 6.7033,
        "altitude_min": 1312,
        "altitude_max": 2800,
        "km_slopes": 100,
        "lifts_count": 23,
        "website": "https://www.bardonecchiaski.com"
    },
    {
        "name": "Limone Piemonte",
        "alternative_names": "Limone, Riserva Bianca",
        "region": "piemonte",
        "province": "Cuneo",
        "lat": 44.2033,
        "lng": 7.5750,
        "altitude_min": 1010,
        "altitude_max": 2050,
        "km_slopes": 80,
        "lifts_count": 15,
        "website": "https://www.rfrski.com"
    },
    {
        "name": "Alagna Valsesia - Monterosa Ski",
        "alternative_names": "Alagna, Valsesia, Monterosa, Monte Rosa, Gressoney",
        "region": "piemonte",
        "province": "Vercelli",
        "lat": 45.8517,
        "lng": 7.9383,
        "altitude_min": 1212,
        "altitude_max": 3275,
        "km_slopes": 180,
        "lifts_count": 38,
        "website": "https://www.monterosa-ski.com"
    },
    
    # VALLE D'AOSTA
    {
        "name": "Cervinia - Breuil-Cervinia",
        "alternative_names": "Cervinia, Breuil, Cervino, Matterhorn, Zermatt, Valtournenche",
        "region": "valle_aosta",
        "province": "Aosta",
        "lat": 45.9333,
        "lng": 7.6333,
        "altitude_min": 2050,
        "altitude_max": 3883,
        "km_slopes": 150,
        "lifts_count": 23,
        "website": "https://www.cervinia.it"
    },
    {
        "name": "Courmayeur",
        "alternative_names": "Courmayeur Mont Blanc, Monte Bianco, La Thuile",
        "region": "valle_aosta",
        "province": "Aosta",
        "lat": 45.7917,
        "lng": 6.9700,
        "altitude_min": 1224,
        "altitude_max": 2755,
        "km_slopes": 100,
        "lifts_count": 18,
        "website": "https://www.courmayeur-montblanc.com"
    },
    {
        "name": "La Thuile",
        "alternative_names": "Thuile, La Rosière, San Bernardo",
        "region": "valle_aosta",
        "province": "Aosta",
        "lat": 45.7167,
        "lng": 6.9500,
        "altitude_min": 1441,
        "altitude_max": 2641,
        "km_slopes": 160,
        "lifts_count": 38,
        "website": "https://www.lathuile.it"
    },
    {
        "name": "Pila",
        "alternative_names": "Pila Valle d'Aosta, Aosta Pila",
        "region": "valle_aosta",
        "province": "Aosta",
        "lat": 45.6617,
        "lng": 7.3083,
        "altitude_min": 1460,
        "altitude_max": 2752,
        "km_slopes": 70,
        "lifts_count": 13,
        "website": "https://www.pila.it"
    },
    
    # VENETO
    {
        "name": "Cortina d'Ampezzo",
        "alternative_names": "Cortina, Ampezzo, Tofane, Faloria, Cristallo, Olimpiadi 2026",
        "region": "veneto",
        "province": "Belluno",
        "lat": 46.5400,
        "lng": 12.1383,
        "altitude_min": 1224,
        "altitude_max": 2930,
        "km_slopes": 120,
        "lifts_count": 37,
        "website": "https://www.cortina.dolomiti.org"
    },
    {
        "name": "Arabba - Marmolada",
        "alternative_names": "Arabba, Marmolada, Regina delle Dolomiti, Dolomiti Superski",
        "region": "veneto",
        "province": "Belluno",
        "lat": 46.4967,
        "lng": 11.8733,
        "altitude_min": 1602,
        "altitude_max": 3265,
        "km_slopes": 62,
        "lifts_count": 27,
        "website": "https://www.arabba.it"
    },
    {
        "name": "Alleghe - Civetta",
        "alternative_names": "Alleghe, Civetta, Val di Zoldo, Ski Civetta",
        "region": "veneto",
        "province": "Belluno",
        "lat": 46.4117,
        "lng": 12.0217,
        "altitude_min": 1000,
        "altitude_max": 2100,
        "km_slopes": 80,
        "lifts_count": 22,
        "website": "https://www.skicivetta.com"
    },
    {
        "name": "Falcade - San Pellegrino",
        "alternative_names": "Falcade, San Pellegrino, Passo San Pellegrino, Tre Valli",
        "region": "veneto",
        "province": "Belluno",
        "lat": 46.3683,
        "lng": 11.8717,
        "altitude_min": 1350,
        "altitude_max": 2513,
        "km_slopes": 100,
        "lifts_count": 25,
        "website": "https://www.trevalli.it"
    },
    
    # FRIULI-VENEZIA GIULIA
    {
        "name": "Tarvisio",
        "alternative_names": "Tarvisio Ski, Monte Lussari, Sella Nevea, Alpe Adria",
        "region": "friuli",
        "province": "Udine",
        "lat": 46.5050,
        "lng": 13.5867,
        "altitude_min": 754,
        "altitude_max": 1760,
        "km_slopes": 30,
        "lifts_count": 7,
        "website": "https://www.promoturismo.fvg.it"
    },
    {
        "name": "Piancavallo",
        "alternative_names": "Piancavallo Ski, Aviano",
        "region": "friuli",
        "province": "Pordenone",
        "lat": 46.1617,
        "lng": 12.5217,
        "altitude_min": 1267,
        "altitude_max": 1850,
        "km_slopes": 25,
        "lifts_count": 10,
        "website": "https://www.piancavalloski.it"
    },
    {
        "name": "Sella Nevea - Kanin",
        "alternative_names": "Sella Nevea, Kanin, Bovec",
        "region": "friuli",
        "province": "Udine",
        "lat": 46.3750,
        "lng": 13.4817,
        "altitude_min": 1180,
        "altitude_max": 2293,
        "km_slopes": 30,
        "lifts_count": 9,
        "website": "https://www.sellaneveakanin.eu"
    },
    
    # EMILIA-ROMAGNA
    {
        "name": "Corno alle Scale",
        "alternative_names": "Corno Scale, Lizzano in Belvedere, Appennino Tosco-Emiliano",
        "region": "emilia",
        "province": "Bologna",
        "lat": 44.1317,
        "lng": 10.8350,
        "altitude_min": 1330,
        "altitude_max": 1945,
        "km_slopes": 30,
        "lifts_count": 8,
        "website": "https://www.cornoallescale.net"
    },
    {
        "name": "Cimone",
        "alternative_names": "Monte Cimone, Sestola, Fanano, Riolunato, Montecreto, Appennino Modenese",
        "region": "emilia",
        "province": "Modena",
        "lat": 44.1933,
        "lng": 10.7017,
        "altitude_min": 1200,
        "altitude_max": 2165,
        "km_slopes": 50,
        "lifts_count": 21,
        "website": "https://www.cimone.it"
    },
    
    # TOSCANA
    {
        "name": "Abetone",
        "alternative_names": "Abetone Multipass, Val di Luce, Appennino Pistoiese",
        "region": "toscana",
        "province": "Pistoia",
        "lat": 44.1467,
        "lng": 10.6667,
        "altitude_min": 1388,
        "altitude_max": 1940,
        "km_slopes": 50,
        "lifts_count": 21,
        "website": "https://www.multipassabetone.it"
    },
    
    # ABRUZZO
    {
        "name": "Roccaraso - Rivisondoli",
        "alternative_names": "Roccaraso, Rivisondoli, Aremogna, Alto Sangro, Pescocostanzo",
        "region": "abruzzo",
        "province": "L'Aquila",
        "lat": 41.8450,
        "lng": 14.0817,
        "altitude_min": 1290,
        "altitude_max": 2141,
        "km_slopes": 130,
        "lifts_count": 31,
        "website": "https://www.skipassaltosangro.it"
    },
    {
        "name": "Campo Felice",
        "alternative_names": "Campo Felice, Rocca di Cambio, L'Aquila",
        "region": "abruzzo",
        "province": "L'Aquila",
        "lat": 42.2317,
        "lng": 13.5417,
        "altitude_min": 1410,
        "altitude_max": 2064,
        "km_slopes": 40,
        "lifts_count": 8,
        "website": "https://www.campofelice.it"
    },
    {
        "name": "Campo Imperatore",
        "alternative_names": "Gran Sasso, Piccolo Tibet d'Italia, L'Aquila",
        "region": "abruzzo",
        "province": "L'Aquila",
        "lat": 42.4467,
        "lng": 13.5583,
        "altitude_min": 1500,
        "altitude_max": 2205,
        "km_slopes": 25,
        "lifts_count": 5,
        "website": "https://www.campoimperatore.it"
    },
    
    # SVIZZERA (vicino al confine)
    {
        "name": "Zermatt",
        "alternative_names": "Zermatt-Cervinia, Matterhorn, Cervino, Klein Matterhorn",
        "region": "svizzera",
        "province": "Vallese",
        "lat": 46.0167,
        "lng": 7.7500,
        "altitude_min": 1620,
        "altitude_max": 3883,
        "km_slopes": 200,
        "lifts_count": 52,
        "website": "https://www.zermatt.ch"
    },
    {
        "name": "St. Moritz",
        "alternative_names": "Saint Moritz, San Moritz, Engadina, Engadin",
        "region": "svizzera",
        "province": "Grigioni",
        "lat": 46.4968,
        "lng": 9.8386,
        "altitude_min": 1720,
        "altitude_max": 3057,
        "km_slopes": 350,
        "lifts_count": 56,
        "website": "https://www.stmoritz.com"
    },
    
    # FRANCIA (vicino al confine)
    {
        "name": "Chamonix",
        "alternative_names": "Chamonix-Mont-Blanc, Monte Bianco, Aiguille du Midi",
        "region": "francia",
        "province": "Alta Savoia",
        "lat": 45.9237,
        "lng": 6.8694,
        "altitude_min": 1035,
        "altitude_max": 3842,
        "km_slopes": 170,
        "lifts_count": 45,
        "website": "https://www.chamonix.com"
    },
    
    # AUSTRIA (vicino al confine)
    {
        "name": "Ischgl",
        "alternative_names": "Ischgl Silvretta, Paznaun, Samnaun",
        "region": "austria",
        "province": "Tirolo",
        "lat": 46.9694,
        "lng": 10.2917,
        "altitude_min": 1400,
        "altitude_max": 2872,
        "km_slopes": 239,
        "lifts_count": 45,
        "website": "https://www.ischgl.com"
    },
    {
        "name": "Sölden",
        "alternative_names": "Solden, Ötztal, Otztal, Obergurgl",
        "region": "austria",
        "province": "Tirolo",
        "lat": 46.9667,
        "lng": 10.8667,
        "altitude_min": 1350,
        "altitude_max": 3340,
        "km_slopes": 144,
        "lifts_count": 31,
        "website": "https://www.soelden.com"
    },
]


class Command(BaseCommand):
    help = 'Popola il database con i principali impianti sciistici italiani e dei paesi confinanti'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Cancella tutti gli impianti esistenti prima di inserire i nuovi',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted_count, _ = SkiResort.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cancellati {deleted_count} impianti esistenti'))

        created_count = 0
        updated_count = 0

        for resort_data in SKI_RESORTS_DATA:
            resort, created = SkiResort.objects.update_or_create(
                name=resort_data['name'],
                defaults=resort_data
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Completato! Creati: {created_count}, Aggiornati: {updated_count}'
        ))
        self.stdout.write(f'Totale impianti nel database: {SkiResort.objects.count()}')
