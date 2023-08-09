![logot](images/tosipaikka_logot.png)

# tosipaikka-decawave-reader

Sovellus lukee USB-portin kautta etäisyysmittauksia ja sijaintitietoa Decawave MDEK1001 -sisätilapaikannusjärjestelmän tunniste-moduulista.

Sovelluksessa on mahdollista laskea moduulin sijainti etäisyysmittauksista laajennetun Kalman suotimen avulla tai käyttää järjestelmän itse laskemaa sijaintia.

Sovellus muuttaa sijainnin WGS84-järjestelmän pituus- ja leveysasteiksi, jotta moduulin sijaintia voidaa visualisoida ulkoisessa karttasovelluksessa. Sijainnin lähetys tapahtuu erillisen MQTT-palvelimen kautta.

Sijaintia voidaan visualisoida esimerkiksi hankkeessa aiemmin tehdyllä verkkosovelluksella:
[https://github.com/SeAMKedu/tosipaikka-indoor-positioning](https://github.com/SeAMKedu/tosipaikka-indoor-positioning)

## Decawave MDEK1001

Kuvassa 1 on kuva Decawave MDEK1001 (**M**odule **D**evelopment & **E**valuation **K**it for the Decawave DWM**1001**) -sisätilapaikannusjärjestelmän moduuleista. Kukin moduuli voidaan konfiguroida ankkuriksi (tukiasemaksi), tunnisteeksi (tagiksi) tai Raspberry Pi:n IO-liittimiin liitettäväksi silta-moduuliksi.

![mdek1001](/images/laitteisto.jpg)

**Kuva 1.** Laitteisto. Silta-moduuli on alarivissä keskellä.

Jokainen Decawave-moduuli sisältää **Positioning And Networking Stack (PANS)** -laiteohjelmiston, jonka avulla ulkoinen sovellus voi kommunikoida moduulin kanssa. Tässä sovelluksessa on hyödynnetty *les*-komentoa, joka palauttaa kunkin ankkurin etäisyysmittaukset ja niiden perusteella lasketun tunniste-moduulin sijainnin.

Alla on esimerkki *les*-komennon palauttamasta datasta.
```
14A6[-3.00,-4.17,0.00]=1.95 9D84[1.00,-4.17,0.00]=3.19 1539[-3.00,3.95,0.00]=7.58 1B95[1.00,3.95,0.00]=7.96 le_us=2868 est[-1.78,-3.40,1.33,29]
```
Yllä olevassa esimerkkidatassa
* 14A6, 9D84, 1539, ja 1B95 ovat ankkurien ID-tunnuksia
* hakasulkujen sisällä on ankkurien koordinaatit metreinä
* yhtäsuuruus-merkin jälkeen on mitattu etäisyys tunniste-moduuliin metreinä
* est[-1.78,-3.40,1.33,29] on tunniste-moduulin laskettu sijainti muodossa [x,y,z,qualityFactor]

## Esivalmistelut

Jos haluat visualisoida tunniste-moduulin sijaintia ulkoisessa karttasovelluksessa, valitse sisätilapaikannusjärjestelmälle origo, jonka pituus- ja leveysasteet on tiedossa. Asettele ankkurit paikoilleen ja mittaa niiden etäisyys suhteessa origoon.

Ankkurien koordinaatit voidaan asettaa helpoiten Android-sovelluksella, jonka saa ladattua APK-tiedostona osoitteesta
[https://www.qorvo.com/products/p/MDEK1001#documents](https://www.qorvo.com/products/p/MDEK1001#documents).

Avaa [config.py](/config.py) tiedosto ja tarkista seuraavat asiat:
* Ankkurien koordinaatit (= samat koordinaatit mitä Android-sovelluksella on määritetty)
* Sisätilapaikannusjärjestelmän koordinaatiston origon pituus- ja leveysasteet
* MQTT-palvelimen IP-osoite, portti, ja topic, jonne sijainti lähetään

Asenna tarvittavat ohjelmistoriippuvuudet komennolla:
```
pip install -r requirements.txt
```

## Sovelluksen ajaminen

Käynnistä sovellus komennolla:
```
python app.py
```

Sovellus voidaan lopettaa näppäinyhdistelmällä Ctrl+c.

## Tekijätiedot

Hannu Hakalahti, Asiantuntija TKI, Seinäjoen ammattikorkeakoulu

## TosiPaikka-hanke

Tämä sovellus on kehitetty osana Tosiaikaisen paikkadatan hyödyntäminen teollisuudessa (TosiPaikka) -hanketta, jota rahoittaa Etelä-Pohjanmaan liitto (EAKR). Lisätietoja hankkeesta löytyy hankkeen kotisuvuilta:

[https://projektit.seamk.fi/alykkaat-teknologiat/tosipaikka/](https://projektit.seamk.fi/alykkaat-teknologiat/tosipaikka/)

