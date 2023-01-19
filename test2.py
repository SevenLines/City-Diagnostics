import os
import subprocess
from shutil import copyfile

roads = [
  {
    "Name": "Автомобильная дорога в 102 микрорайон (ул. Ринчино)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Rinchino\\2019.10.11_14-36_UU_Rinchino_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога в 113 микрорайон",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_113 mkr\\2019.10.11_14-14_UU_113 mkr_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога в п. Сокол",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Sokol\\2019.10.13_14-38_UU_Sokol_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога в с. Поселье",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Poselie\\2019.10.13_14-56_UU_Poselie_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога к мкр. Старый Зеленый",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Stariy Zeleniy\\2019.10.14_16-44_UU_Stariy Zeleniy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога от 102 квартала до 118 квартала",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_ot 102 do 118\\2019.10.11_15-07_UU_ot 102 do 118_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога от ул. Ботаническая до 13 км",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_ot Botanicheskaya do 13 km\\2019.10.17_12-34_UU_ot Botanicheskaya do 13 km_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога п. Матросова от ул. Н. Нищенко до п. Полигон, 8а",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_pos Matrosova\\2019.10.14_17-10_UU_pos Matrosova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога перекресток ул. Жердева и ул. Шумяцкого",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_perekrestok Zherdeva\\2019.10.12_18-51_UU_perekrestok Zherdeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по бульвару К. Маркса",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_bul K Marksa_Pavlova\\2019.10.11_17-13_UU_bul K Marksa_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по бульвару К. Маркса_2уч",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_bul K Marksa_Pavlova\\2019.10.11_17-13_UU_bul K Marksa_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по пер. Герцена",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Gercena_Stolichnaya_Krasnodonskaya\\2019.10.14_13-48_UU_Gercena_Stolichnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по пер. Невского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Nevskogo\\2019.10.14_13-22_UU_Nevskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по пер. Толстого",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_per Tolstogo\\2019.10.12_15-36_UU_per Tolstogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по пр. 50-летия Октября",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_50letiya Oktyabrya_Limonova\\2019.10.13_13-36_UU_50letiya Oktyabrya_Limonova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по пр. Автомобилистов",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_Boevaya_Stroiteley_Avtomobilistov\\2019.10.17_11-12_UU_Boevaya_Stroiteley_Avtomobilistov_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по пр. Строителей",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_Boevaya_Stroiteley_Avtomobilistov\\2019.10.17_11-12_UU_Boevaya_Stroiteley_Avtomobilistov_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Акмолинская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Akmolinskaya\\2019.10.13_11-40_UU_Akmolinskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Барнаульская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Barnaulskaya\\2019.10.15_14-21_UU_Barnaulskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Воронежская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Voronezhskaya\\2019.10.13_12-08_UU_Voronezhskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Гарнаева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Garnaeva\\2019.10.14_14-01_UU_Garnaeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Каландаришвили",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Kalandarishvili\\2019.10.12_14-01_UU_Kalandarishvili_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Калашникова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Kalashnikova\\2019.10.14_17-53_UU_Kalashnikova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Кундо",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Kundo\\2019.10.13_12-03_UU_Kundo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Ленина (1 участок)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Lenina\\2019.10.12_13-13_UU_Lenina1_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Ленина (2 участок)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Lenina\\2019.10.12_12-16_UU_Lenina3_Lenina2_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Ленина (3 участок)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Lenina\\2019.10.12_12-16_UU_Lenina3_Lenina2_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Медицинская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Medecinskaya_Krasnoy Zvezdi\\2019.10.11_16-03_UU_Medecinskaya_Krasnoy Zvezdi_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Михалева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Mihaleva\\2019.10.13_15-11_UU_Mihaleva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Мостовая",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Mostovaya\\2019.10.11_11-13_UU_Mostovaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Моцарта",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Mocarta\\2019.10.14_14-07_UU_Mocarta_zaaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Производственная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Proizvodstvennaya\\2019.10.11_11-26_UU_Proizvodstvennaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Псковская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_Pskovskaya\\2019.10.17_17-14_UU_Pskovskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Стартовая",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Startovaya\\2019.10.13_14-25_UU_Startovaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Столбовая (1)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Stolbovaya\\2019.10.15_12-36_UU_Stolbovaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Столбовая (2)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Stolbovaya\\2019.10.15_12-44_UU_Stolbovaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Столбовая (3)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Stolbovaya\\2019.10.15_12-49_UU_Stolbovaya_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Столбовая (6)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Stolbovaya\\2019.10.15_13-10_UU_Stolbovaya_zaezd6_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Сухэ-Батора",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Suhe-Batora\\2019.10.12_13-32_UU_Suhe-Batora_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Тулаева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Trubacheeva\\2019.10.11_12-18_UU_Trubacheeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Хоринская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Horinskaya\\2019.10.14_14-32_UU_Horinskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Чайковского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Chaykovskogo\\2019.10.14_15-55_UU_Chaykovskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Широких-Полянского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Shirokih-Polyanskogo\\2019.10.11_11-46_UU_Shirokih-Polyanskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Боевая",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_Boevaya_Stroiteley_Avtomobilistov\\2019.10.17_11-12_UU_Boevaya_Stroiteley_Avtomobilistov_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Воровского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Vorovskogo\\2019.10.12_15-16_UU_Vorovskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Гармаева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Lebedeva_Pugacheva_Garmaeva\\2019.10.13_16-26_UU_Lebedeva_Pugacheva_Garmaeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Гастелло",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Gastello\\2019.10.14_14-26_UU_Gastello_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Гоголя",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Gogolya_Dalnenagornaya_Lazo\\2019.10.12_16-39_UU_Gogolya_Dalnenagornaya_Lazo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Дальненагорной",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Gogolya_Dalnenagornaya_Lazo\\2019.10.12_16-39_UU_Gogolya_Dalnenagornaya_Lazo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Димитрова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Dimitrova\\2019.10.12_15-28_UU_Dimitrova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Дорожная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Ivolginskaya_Dorozhnaya\\2019.10.13_14-04_UU_Ivolginskaya_Dorozhnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Ермаковской",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Ermakovskoy\\2019.10.12_15-44_UU_Ermakovskoy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Жанаева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Zhanaeva\\2019.10.12_15-56_UU_Zhanaeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Заиграевская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Zaigraevskaya\\2019.10.14_16-19_UU_Zaigraevskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Иволгинская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Ivolginskaya_Dorozhnaya\\2019.10.13_14-04_UU_Ivolginskaya_Dorozhnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Камова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Kamova\\2019.10.14_15-44_UU_Kamova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Кирова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Kirova\\2019.10.12_12-53_UU_Kirova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Коммунистическая",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Kommunisticheskaya\\2019.10.12_14-11_UU_Kommunisticheskaya_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Королева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Koroleva\\2019.10.14_15-09_UU_Koroleva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Краснодонская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Gercena_Stolichnaya_Krasnodonskaya\\2019.10.14_13-42_UU_Krasnodonskaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Красной Звезды",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Medecinskaya_Krasnoy Zvezdi\\2019.10.11_16-03_UU_Medecinskaya_Krasnoy Zvezdi_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Крылова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Krilova\\2019.10.12_18-28_UU_Krilova_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Крылова_2 уч",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Krilova\\2019.10.12_18-28_UU_Krilova_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Куйбышева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Naberezhnoy_Smolina_Kuybisheva\\2019.10.12_14-40_UU_Kuybisheva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Лазо",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Gogolya_Dalnenagornaya_Lazo\\2019.10.12_16-39_UU_Gogolya_Dalnenagornaya_Lazo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Лебедева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Lebedeva_Pugacheva_Garmaeva\\2019.10.13_16-26_UU_Lebedeva_Pugacheva_Garmaeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Лимонова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_50letiya Oktyabrya_Limonova\\2019.10.13_13-36_UU_50letiya Oktyabrya_Limonova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Микояна",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Mikoyana\\2019.10.14_15-23_UU_Mikoyana_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Модогоева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Modogoeva\\2019.10.12_13-24_UU_Modogoeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Мунгонова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Mungonova\\2019.10.14_15-01_UU_Mungonova_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Набережной",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Naberezhnoy_Smolina_Kuybisheva\\2019.10.12_11-41_UU_Naberezhnoy_Smolina_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Намжилова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Namzhilova\\2019.10.12_18-38_UU_Namzhilova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Окинской",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Okinskoy\\2019.10.13_15-53_UU_Okinskoy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Оцимика",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Ocimika\\2019.10.12_16-02_UU_Ocimika_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Пугачева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Lebedeva_Pugacheva_Garmaeva\\2019.10.13_16-26_UU_Lebedeva_Pugacheva_Garmaeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Родины",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Rodini\\2019.10.14_14-15_UU_Rodini_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Родины_кольцо",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Rodini\\2019.10.14_14-15_UU_Rodini_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Смолина",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Naberezhnoy_Smolina_Kuybisheva\\2019.10.12_11-41_UU_Naberezhnoy_Smolina_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Советская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Sovetskaya\\2019.10.12_12-35_UU_Sovetskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Спартака",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Spartaka_Pirogova\\2019.10.11_17-32_UU_Spartaka_Pirogova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Степная Протока",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\18\\UU_Stepnaya\\2019.10.13_15-41_UU_Stepnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Столичная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Gercena_Stolichnaya_Krasnodonskaya\\2019.10.14_13-48_UU_Gercena_Stolichnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Тобольской",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Zherdeva_Tobolskoy\\2019.10.12_17-33_UU_Zherdeva_Tobolskoy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Толстого",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Tolstogo\\2019.10.12_15-05_UU_Tolstogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Туполева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Tupoleva\\2019.10.14_15-14_UU_Tupoleva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Цыбикова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Cybikova\\2019.10.11_17-01_UU_Cybikova_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Чкалова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Chkalova\\2019.10.14_15-27_UU_Chkalova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Шумяцкого",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Trubacheeva\\2019.10.11_12-18_UU_Trubacheeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Больничная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Bolnichnaya\\2019.10.11_16-24_UU_Bolnichnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Гражданская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Grazhdanskaya\\2019.10.11_11-34_UU_Grazhdanskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Дальневосточная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Dalnevostochnaya_Sovhoznaya\\2019.10.15_13-32_UU_Dalnevostochnaya_Sovhoznaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Жердева (2.33)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Zherdeva_Tobolskoy\\2019.10.12_17-33_UU_Zherdeva_Tobolskoy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Жердева (кусочек)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Trubacheeva\\2019.10.11_12-18_UU_Trubacheeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Кольцова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Trubacheeva\\2019.10.11_12-18_UU_Trubacheeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Конечная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Konechnaya\\2019.10.14_17-45_UU_Konechnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Красногвардейская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Krasnogvardeyskaya\\2019.10.11_12-07_UU_Krasnogvardeyskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Орловская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Orlovskaya\\2019.10.11_15-36_UU_Orlovskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Павлова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_bul K Marksa_Pavlova\\2019.10.11_17-39_UU_Pavlova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Пирогова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Spartaka_Pirogova\\2019.10.11_17-32_UU_Spartaka_Pirogova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Пищевая",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_Pischevaya_ot zhd pereezda\\2019.10.18_17-11_UU_Pischevaya_ot zhd pereezda_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Трубачеева",
    "path": "F:\\16\\UU_Trubacheeva\\2019.10.11_12-18_UU_Trubacheeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Дарханская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\17\\UU_Darhanskaya\\2019.10.12_17-57_UU_Darhanskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Мокрова - п. Энергетик",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Mokrova\\2019.10.15_11-39_UU_Mokrova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "ул. Глинки",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\19\\UU_Glinki\\2019.10.14_13-12_UU_Glinki_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Кузнецкая (от ул. Бабушкина до ул. Красной Звезды)",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Kuznetskaya\\2019.10.11_15-48_UU_Kuznetskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Реконструкция автодороги от ул. Орловская мкр. Горький до въезда в г. Улан-Удэ",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_ot Orlovskaya\\2019.10.11_13-32_UU_ot Orlovskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Ремонт дороги с устройством тротуара по ул. Ключевская от ост",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Trubacheeva\\2019.10.11_12-18_UU_Trubacheeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Ремонт дороги Спиртзаводской тракт от ул. Пищевая до 0-го км",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_Spirtzavodskoy trakt\\2019.10.18_16-47_UU_Spirtzavodskoy trakt_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога от ул. Ботаническая до 13 км автомобильной дороги Улан-Удэ-Турунтаево-Курумкан-Новый Уоян к этнографическому музею",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_k muzeyu\\2019.10.17_12-55_UU_k muzeyu_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Шевченко, Олимпийский переулок, ул. 3-я Кедровая, ул. Дарвина",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\23\\UU_Olympiyskiy per\\2019.10.17_15-39_UU_Olympiyskiy per_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автодорога по ул. Норильская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Norilskaya\\2019.10.16_13-43_UU_Norilskaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автодорога по ул. Сенчихина",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Senchihina\\2019.10.16_16-39_UU_Senchihina_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Шульца",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Shulca\\2019.10.16_16-22_UU_Shulca_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Амагаева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Belinskogo_Amagaeva\\2019.10.16_11-38_UU_Belinskogo_Amagaeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Белинского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Belinskogo_Amagaeva\\2019.10.16_11-38_UU_Belinskogo_Amagaeva_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Буйко",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Buyko\\2019.10.16_14-05_UU_Buyko_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Выборгская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Viborgskaya\\2019.10.16_12-39_UU_Viborgskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Гвардейская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Gvardeyskaya\\2019.10.16_12-47_UU_Gvardeyskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Д. Бедного",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_D Bednogo\\2019.10.16_16-51_UU_D Bednogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Дарвина",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Darvina\\2019.10.16_12-18_UU_Darvina_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Дзержинского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Dobrolyubova_Dzerzhinskogo\\2019.10.16_15-35_UU_Dobrolyubova_Dzerzhinskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Добролюбова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Dobrolyubova_Dzerzhinskogo\\2019.10.16_15-35_UU_Dobrolyubova_Dzerzhinskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Жуковского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Zhukovskogo\\2019.10.16_17-44_UU_Zhukovskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Комсомольской",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Komsomolskaya\\2019.10.16_14-33_UU_Komsomolskaya_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Майская",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Mayskaya\\2019.10.16_16-45_UU_Mayskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Маяковского",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Mayakovskogo\\2019.10.16_14-46_UU_Mayakovskogo_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Пестеля",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Pestelya\\2019.10.16_15-15_UU_Pestelya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. проезду Бальбурова",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Balburova\\2019.10.16_13-58_UU_Balburova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Путейская 1",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Puteyskaya\\2019.10.16_16-34_UU_Puteyskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Путейская 2",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Puteyskaya\\2019.10.16_16-34_UU_Puteyskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Путейская 3",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Puteyskaya\\2019.10.16_16-34_UU_Puteyskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Сосновая",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Sosnovaya\\2019.10.16_14-10_UU_Sosnovaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Хоца Намсараева",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Hoca Namsaraeva\\2019.10.16_15-03_UU_Hoca Namsaraeve_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Целинная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Celinnaya\\2019.10.16_13-10_UU_Celinnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Чертенкова 1",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Yunogo Kommunara_Chertenkova\\2019.10.16_15-51_UU_Yunogo Kommunara_Chertenkova_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Чертенкова 2",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Yunogo Kommunara_Chertenkova\\2019.10.16_15-51_UU_Yunogo Kommunara_Chertenkova_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Шевченко",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Shevchenko\\2019.10.16_12-00_UU_Shevchenko_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Юннатов",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Yunnatov\\2019.10.16_13-16_UU_Yunnatov_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Юного Коммунара",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Yunogo Kommunara_Chertenkova\\2019.10.16_15-51_UU_Yunogo Kommunara_Chertenkova_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Пушкина 1",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Pushkina\\2019.10.16_18-06_UU_Pushkina_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Пушкина 2",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Pushkina\\2019.10.16_18-06_UU_Pushkina_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Пушкина 3",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\21\\UU_Pushkina\\2019.10.16_18-06_UU_Pushkina_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Совхозная",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\20\\UU_Dalnevostochnaya_Sovhoznaya\\2019.10.15_13-32_UU_Dalnevostochnaya_Sovhoznaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога от жд переезда (птицефабрика) до ул. Ильинская пос. Тальцы",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Pskovskaya_Talci\\2019.10.17_13-50_UU_Pskovskaya_Talci_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога от ул.  Комарова до 0-го км",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Petrova_11_7_Blinova_Komarova\\2019.10.14_11-46_UU_Petrova_11_7_Blinova_Komarova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога перекресток ул. Н. Петрова и ул. Комсомольская",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Petrova_11_7_Blinova_Komarova\\2019.10.14_11-46_UU_Petrova_11_7_Blinova_Komarova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по второстепенным проездам по пр. Автомобилистов_1",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Avtomobilistov vtor proezdy\\2019.10.21_11-55_UU_Avtomobilistov vtor proezdy_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по второстепенным проездам по пр. Автомобилистов_2",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Avtomobilistov vtor proezdy\\2019.10.21_11-55_UU_Avtomobilistov vtor proezdy_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. 40 лет Победы",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_40 let Pobedy\\2019.10.21_13-03_UU_40 let Pobedy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Блинова",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Petrova_11_7_Blinova_Komarova\\2019.10.14_11-46_UU_Petrova_11_7_Blinova_Komarova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Керамическая",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.13_10-52_UU_Borsoeva_Keramicheskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Левченко",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.13_12-46_UU_Revolucii_Levchenko_Sotnikovskaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Октябрьская",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Oktyabrskaya\\2019.10.19_12-15_UU_Oktyabrskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Цивилева",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Civileva_8\\2019.10.19_11-33_UU_Civileva_8_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. 3-я Транспортная",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_3ya Transportnaya\\2019.10.19_12-44_UU_3ya Transportnaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. 502 км 1",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_502 km\\2019.10.19_14-00_UU_502 km_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. 502 км 2",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_502 km\\2019.10.19_14-00_UU_502 km_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Борсоева_1",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.19_11-19_UU_Borsoeva_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Борсоева_2",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.19_11-19_UU_Borsoeva_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Борсоева_3 обр",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.19_11-19_UU_Borsoeva_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Борсоева_3",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.19_11-19_UU_Borsoeva_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Борсоева_4",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.19_11-19_UU_Borsoeva_zaezd3_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Гагарина",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Gagarina\\2019.10.19_11-43_UU_Gagarina_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Калинина",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Kalinina\\2019.10.19_11-07_UU_Kalinina_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Красноармейская",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Krasnoarmeyskaya\\2019.10.19_12-03_UU_Krasnoarmeyskaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Н. Петрова",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Petrova_11_7_Blinova_Komarova\\2019.10.14_11-46_UU_Petrova_11_7_Blinova_Komarova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. ул. Моховая",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Mohovaya\\2019.10.19_13-20_UU_Mohovaya_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. ул. Шаляпина",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Shalyapina\\2019.10.19_13-00_UU_Shalyapina_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Хахалова",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Hahalova\\2019.10.19_11-24_UU_Hahalova_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Революции 1905 г. от пр. 50-летия Октября до ул. Левченко_1",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.13_12-46_UU_Revolucii_Levchenko_Sotnikovskaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Революции 1905 г. от пр. 50-летия Октября до ул. Левченко_2",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.13_12-46_UU_Revolucii_Levchenko_Sotnikovskaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Революции 1905 г. от пр. 50-летия Октября до ул. Левченко_3",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.13_12-46_UU_Revolucii_Levchenko_Sotnikovskaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога ул. Тепловой от АЗС Витлас до примыкания к ул. Лесной",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\24\\UU_Teplovaya\\2019.10.21_12-13_UU_Teplovaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Ремонт дороги по ул. Сотниковская от ул. Радикальцева до ул. Каменная",
    "path": "F:\\_ROADS\\ULAN_UDE2019\\25\\UU_Revolucii_Levchenko_Sotnikovskay_Borsoeva\\2019.10.13_12-46_UU_Revolucii_Levchenko_Sotnikovskaya_zaezd2_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Сахьяновой",
    "path": "D:\\__\\_2\\UU_Sahyanovoy\\2019.10.31_11-58_UU_Sahyanovoy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Автомобильная дорога по ул. Терешковой",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Tereshkovoy\\2019.10.11_17-56_UU_Tereshkovoy_zaezd1_pryamo\\Cam7.dav"
  },
  {
    "Name": "Ремонт дороги с устройством тротуара по ул. Ключевская от ост",
    "path": "E:\\_ROADS\\ULAN_UDE2019\\16\\UU_Trubacheeva\\2019.10.11_12-18_UU_Trubacheeva_zaezd1_pryamo\\Cam7.dav"
  }
]

if __name__ == '__main__':
    for r in roads:
        splited = r['path'].split("\\")
        path = "\\".join(splited[-4:-1])
        path_avi_source = os.path.join("e:\\_ROADS\\ULAN_UDE2019\\", path, "Cam1.dav")
        path_avi_target = os.path.join("d:\\_ROADS\\ULAN_UDE_2019_VIDEO\\", "{}.dav".format(r["Name"]))
        path_smi_source = os.path.join("e:\\_ROADS\\ULAN_UDE2019\\", path, "Cam1.smi")
        path_smi_target = os.path.join("d:\\_ROADS\\ULAN_UDE_2019_VIDEO\\", "{}.smi".format(r["Name"]))
        # if not os.path.exists(path_avi_source):
        try:
            copyfile(path_avi_source, path_avi_target)
            copyfile(path_smi_source, path_smi_target)
        except Exception as ex:
            print(path_avi_source)
