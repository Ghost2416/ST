import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_folium as st_folium
from streamlit_folium import folium_static
import json
import folium
from folium import Popup
from folium import plugins
from PIL import Image

#J'importe le DataFrame final après traitement sur Jupyter Notebook
df=pd.read_csv("C:\\Users\\Triss\\Documents\\World_Happiness_Project\\df_final.csv")

#Je nomme mes pages et mon sommaire
st.title("Projet d'Analyse du bonheur dans le monde")
st.sidebar.title("Sommaire")
pages=["Exploration", "DataVizualization", "Rapport"]
page=st.sidebar.radio("Aller vers", pages)

#Constitution de la page 1
if page == pages[0] : 
  st.write("### Introduction")
  st.dataframe(df.head(5))
  st.write(df.shape)
  st.dataframe(df.describe())

  if st.checkbox("Afficher les NA") :
    st.dataframe(df.isna().sum())

#Constitution de la page 2
if page == pages[1] :
  st.write("### DataVizualization")
  st.subheader("Barplot des variables explicatives")

#Constitution d'un échantillon de plusieurs pays sur tous les continents afin de tenter une représentation Barplot
  target = ["France", "Germany", "Switzerland", "Belgium", "Spain", "Czech Republic", "Ukraine", "Poland", "Romania", "Hungary", "Algeria", "Morocco", "Tunisia", "Congo (Brazzaville)",
  "Gabon", "Cameroon", "South Africa", "Namibia", "Botswana", "Swaziland", "Uzbekistan", "Pakistan", "Bangladesh", "China", "Japan", "South Korea", "Taiwan Province of China",
  "Hong Kong S.A.R. of China", "New Zealand", "Australia", "Canada", "United States", "Costa Rica", "Guatemala", "Mexico", "Jamaica", "Panama", "El Salvador", "Nicaragua", "Honduras",
  "Brazil", "Uruguay", "Chile", "Argentina", "Ecuador", "Bolivia", "Paraguay", "Venezuela", "Colombia", "Peru", "Russia"]

  df_target = df[df['Country name'].isin(target)]

  variables = ['Ladder score', 'Logged GDP per capita', 'Social support',
             'Healthy life expectancy', 'Freedom to make life choices',
             'Generosity', 'Perceptions of corruption']

  for var in variables:
    plt.figure(figsize=(15, 7))
    sorted_countries = df_target.sort_values(by=var, ascending=False)['Country name']
    sns.barplot(x='Country name', y=var, data=df_target, palette='viridis', order=sorted_countries)
    plt.title(var)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

  texte = """
  Sur l’analyse des graphiques en barre on s'aperçoit que le premier échantillon qui concerne un certain nombre de tous les continents on peut établir un classement qui n’est pas strict mais qui serait: Europe, Amérique latine, Asie et Afrique pour le Ladder Score.
  On remarque ici que les pays développés sont en tête de liste dans notre échantillon.
  Pour le social support on s'aperçoit que cela suit la tendance du Logged per capita, ce qui peut sembler logique. Le fait d’avoir de l’argent donne un sentiment d’être soutenu dans l’échelle social.
  L’espérance de vie est assez stable et baisse considérablement pour les pays d’Afrique noire et le Pakistan, on peut interpréter que cela est dû au manque de soin ou d’infrastructures qui permettent de soigner ses habitants.
  En ce qui concerne la liberté on se rend compte que le barplot présente des pays plus hétérogènes on peut se dire que la liberté est une idée propre à chacun.
  Pour notre échantillon sur la générosité on se rend compte que l’on passe très vite en dessous de la moyenne à partir de l’Ukraine, on peut rapidement en déduire que la générosité n’est pas un critère qui influe sur le sentiment de bonheur dans un pays.
  Le sentiment de corruption est très hétérogène dans notre échantillon et on déduit donc que ce critère n’est pas corrélé au bonheur dans le monde.
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte}</div>", unsafe_allow_html=True)  

#Constitution de plusieurs maps interactives afin d'aller chercher l'information
#Map 1 avec dégradé de couleur vert pour le Ladder Score
  st.subheader("Cartes interactives et matrice de corrélation")
  m = folium.Map(location=[0, 0], zoom_start=2)
  with open("C:\\Users\\Triss\\Documents\\World_Happiness_Project\\Base de données\\countries.geojson") as f:
      world_geo = json.load(f)
  folium.Choropleth(
      geo_data=world_geo,
      name='Score du bonheur',
      data=df,
      columns=['Country name', 'Ladder score'],
      key_on='feature.properties.ADMIN',
      fill_color='YlGn',
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name='Score du bonheur par pays'
  ).add_to(m)  

  for index, row in df.iterrows():
      folium.CircleMarker(
          location=[row['Latitude'], row['Longitude']],
          radius=5,
          fill=True,
          fill_opacity=1,
          popup=folium.Popup(
              f"<strong>{row['Country name']}</strong><br>"
              f"Score de bonheur : {row['Ladder score']:.2f}<br>"
              f"PIB par habitant : {row['Logged GDP per capita']:.2f}<br>"
              f"Soutien social : {row['Social support']:.2f}<br>"
              f"Espérance de vie en bonne santé : {row['Healthy life expectancy']:.2f}<br>"
              f"Liberté de faire des choix de vie : {row['Freedom to make life choices']:.2f}<br>"
              f"Générosité : {row['Generosity']:.2f}<br>"
              f"Perception de la corruption : {row['Perceptions of corruption']:.2f}",
              max_width=450
          )
      ).add_to(m)
  folium_static(m)

  texte_1 = """
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte_1}</div>", unsafe_allow_html=True)  

#Matrice de corrélation afin de déterminer le rapport entre le Ladder Score et d'autres variables
  st.set_option('deprecation.showPyplotGlobalUse', False)
  correlation_matrix = df[[
      'Ladder score', 'Social support', 'Freedom to make life choices',
      'Generosity', 'Perceptions of corruption'
  ]].corr()

  plt.figure(figsize=(10, 8))
  sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
  plt.title('Matrice de Corrélation')
  st.pyplot()

  texte_2 = """
Ladder score et Social support : Une forte corrélation positive indique que des scores plus élevés sur l'échelle du bien-être sont étroitement liés à un meilleur soutien social. En d'autres termes, dans les lieux où les gens perçoivent qu'ils ont plus de soutien social, ils tendent aussi à avoir un score plus élevé de bien-être.
Ladder score et Freedom to make life choices : Cette corrélation positive montre que le sentiment de liberté pour faire des choix de vie est assez fortement associé à de meilleurs scores de bien-être.
Ladder score et Perceptions of corruption : Il y a une corrélation négative modérée ici, suggérant que des perceptions plus élevées de corruption sont généralement associées à des scores de bien-être plus faibles.
Social support et Freedom to make life choices : Cette corrélation positive moyenne suggère que les personnes qui ressentent un plus grand soutien social ont tendance à ressentir plus de liberté dans leurs choix de vie.
Social support et Perceptions of corruption : Il existe une corrélation négative faible à modérée, impliquant que plus le soutien social est élevé, moins la corruption est perçue.
Freedom to make life choices et Perceptions of corruption : Une corrélation négative modérée indique que lorsque les gens perçoivent qu'ils ont plus de liberté de choix, il y a généralement moins de perception de corruption.
Generosity a des corrélations faibles ou négligeables avec toutes les autres variables, ce qui indique que la générosité n'est pas fortement liée aux perceptions de bien-être, de soutien social, de liberté de choix ou de corruption dans cet échantillon.
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte_2}</div>", unsafe_allow_html=True) 

#Une map avec plusieurs couches pour les 3 variables les plus corrélées
#Map 2 avec dégradé de couleur et 3 calques
  m = folium.Map(location=[0, 0], zoom_start=2)
  with open("C:\\Users\\Triss\\Documents\\World_Happiness_Project\\Base de données\\countries.geojson") as f:
      world_geo = json.load(f)
  def add_layer(col, name, color):
      choropleth = folium.Choropleth(
          geo_data=world_geo,
          name=name,
          data=df,
          columns=['Country name', col],
          key_on='feature.properties.ADMIN',
          fill_color=color,
          fill_opacity=0.7,
          line_opacity=0.2,
          legend_name=name
      ).add_to(m)
      choropleth.geojson.add_child(
          folium.features.GeoJsonTooltip(['ADMIN'], labels=False)
      )
  add_layer('Ladder score', 'Ladder Score', 'BuGn')
  add_layer('Social support', 'Social Support', 'YlOrRd')
  add_layer('Freedom to make life choices', 'Freedom to Make Life Choices', 'BuPu')
  folium.LayerControl().add_to(m)
  folium_static(m)

  texte_3 = """
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte_3}</div>", unsafe_allow_html=True) 

#Une map avec plusieurs couches pour les 3 variables les moins corrélées
#Map 3 avec dégradé de couleur et 3 calques
  m = folium.Map(location=[0, 0], zoom_start=2)
  with open("C:\\Users\\Triss\\Documents\\World_Happiness_Project\\Base de données\\countries.geojson") as f:
      world_geo = json.load(f)
  def add_layer(col, name, color):
      choropleth = folium.Choropleth(
          geo_data=world_geo,
          name=name,
          data=df,
          columns=['Country name', col],
          key_on='feature.properties.ADMIN',
          fill_color=color,
          fill_opacity=0.7,
          line_opacity=0.2,
          legend_name=name
      ).add_to(m)
      choropleth.geojson.add_child(
          folium.features.GeoJsonTooltip(['ADMIN'], labels=False)
      )
  add_layer('Generosity', 'Generosity', 'BuGn')
  add_layer('Perceptions of corruption', 'Perceptions of corruption', 'YlOrRd')
  add_layer('Healthy life expectancy', 'Healthy life expectancy', 'BuPu')
  folium.LayerControl().add_to(m)
  folium_static(m)

  texte_4 = """
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte_4}</div>", unsafe_allow_html=True) 

#Scatterplot de la relation entre le Ladder Score et les variables explicatives
  st.subheader("Nuages de points relation var exp et Ladder Score")
  variables_explicatives = ['Social support', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption', 'Average Annual Temperature']
  for var in variables_explicatives:
      plt.figure(figsize=(10, 6))
      sns.scatterplot(x=var, y='Ladder score', data=df)
      plt.title(f'Relation entre {var} et Ladder score')
      st.pyplot()

  texte_5 = """
  la liberté de choix est positivement associée à la qualité de vie ou au bonheur, tandis que la corruption est négativement associée. La générosité ne montre pas de tendance claire, ce qui suggère que d'autres facteurs pourraient influencer comment ou si la générosité se traduit par une qualité de vie plus élevée.
  Le support social semble avoir une influence beaucoup plus directe et positive sur le bien-être des individus par rapport à la température annuelle moyenne. Cela peut souligner l'importance des relations sociales et du sentiment d'appartenance à une communauté pour le bonheur des gens, tandis que les conditions climatiques, bien qu'elles puissent affecter le bien-être dans certaines situations, ne semblent pas avoir une relation globale et uniforme avec le niveau de bonheur perçu à l'échelle mondiale.
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte_5}</div>", unsafe_allow_html=True) 


#Barplot des variables explicatives pour les 5 meilleurs pays et les 5 moins bons
  st.subheader("Graphique en barre représentant les var exp pour 5 Top et 5 Bottom")
  top_countries = df.sort_values(by='Ladder score', ascending=False).head(5)
  bottom_countries = df.sort_values(by='Ladder score', ascending=True).head(5)

  combined = pd.concat([top_countries, bottom_countries])
  combined['Type'] = ['Top 5' if country in top_countries['Country name'].values else 'Bottom 5' for country in combined['Country name']]

  plt.figure(figsize=(10, 6))
  sns.barplot(data=combined, x='Country name', y='Ladder score', hue='Type', palette={"Top 5": "skyblue", "Bottom 5": "salmon"})

  plt.title('Top 5 and Bottom 5 Countries by Life Ladder Score')
  plt.xticks(rotation=45, ha='right')
  plt.ylabel('Ladder Score')
  plt.xlabel('Country Name')

  plt.tight_layout()
  plt.legend(title='Type')
  st.pyplot()

  explanatory_vars = [
      'Logged GDP per capita', 
      'Social support', 
      'Healthy life expectancy', 
      'Freedom to make life choices', 
      'Generosity', 
      'Perceptions of corruption'
  ]

  top_countries = df.sort_values(by='Ladder score', ascending=False).head(5)
  bottom_countries = df.sort_values(by='Ladder score', ascending=True).head(5)

  combined = pd.concat([top_countries, bottom_countries])
  combined['Type'] = ['Top 5' if country in top_countries['Country name'].values else 'Bottom 5' for country in combined['Country name']]

  palette = {"Top 5": "skyblue", "Bottom 5": "salmon"}

  for var in explanatory_vars:
      plt.figure(figsize=(10, 6))
      sns.barplot(data=combined, x='Country name', y=var, hue='Type', palette=palette)
        
      plt.title(f'{var} vs Ladder Score for Top 5 and Bottom 5 Countries')
      plt.xticks(rotation=45, ha='right')
      plt.ylabel(var)
      plt.xlabel('Country Name')
        
      plt.tight_layout()
      plt.legend(title='Type')
      st.pyplot()

  texte_6 = """
  L'analyse graphiques montre des tendances cohérentes entre le niveau de satisfaction de vie, la richesse économique, et la perception de la corruption. Les pays avec des scores de satisfaction de vie élevés tendent à avoir un PIB par habitant plus élevé et une perception de la corruption plus faible. Ceci peut suggérer que la stabilité économique et la confiance dans les institutions publiques jouent un rôle important dans le bien-être des citoyens. Inversement, les pays avec des scores de satisfaction de vie plus bas ont un PIB par habitant plus faible et une perception de la corruption plus élevée, ce qui pourrait indiquer des défis plus importants en matière de développement économique et de gouvernance.
  Dans l'ensemble, ces graphiques pourraient suggérer des corrélations entre le Ladder score et diverses dimensions du bien-être telles que la liberté, la générosité et l'espérance de vie en bonne santé. Les données impliquent que les pays les mieux classés performent généralement bien à travers ces indicateurs, tandis que les pays les moins bien classés montrent plus de variation. La générosité du Rwanda est une exception notable, indiquant que malgré des scores globaux plus faibles, certains comportements sociaux positifs peuvent toujours être très prévalents.
  Le graphique du social support suggère fortement que le soutien social est corrélé positivement avec le score d'échelle des pays, ce qui peut être un indicateur de bien-être général. Les pays bien classés bénéficient non seulement d'un soutien social élevé mais cela pourrait aussi contribuer à une meilleure qualité de vie globale. Inversement, les pays moins bien classés pourraient voir leur qualité de vie améliorée si des mesures étaient prises pour augmenter le soutien social parmi leurs citoyens.
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte_6}</div>", unsafe_allow_html=True)

if page == pages[2]:
  st.write("### Rapport final")

  image = Image.open("C:\\Users\\Triss\\Documents\\World_Happiness_Project\\happiness.jpg")
  st.image(image, use_column_width=True)
  st.subheader("Rapport: Facteurs Contribuant au Bien-être National et Propositions pour Améliorer le Ladder Score")

  texte_7 = """
  Contexte:
  D'après l'analyse des données disponibles, il est évident que le bien-être national, tel que mesuré par le Ladder Score, est complexe et multifactoriel. Plusieurs éléments sont fortement liés à cette mesure du bonheur et du bien-être.

  Facteurs Influant sur le Ladder Score:

  Le Support Social:
  Le soutien social est un pilier crucial du bien-être. Il s'avère que les pays avec un fort soutien social ont tendance à enregistrer des scores plus élevés de bien-être. Cela inclut le sentiment d'avoir quelqu'un sur qui compter, la présence d'un réseau de soutien familial ou communautaire, et l'accès à l'aide sociale en cas de besoin.

  Liberté de Choix:
  La liberté individuelle de faire des choix de vie est étroitement liée à un meilleur bien-être. La possibilité de choisir son chemin de vie, d'exercer un contrôle sur ses propres actions et de prendre des décisions personnelles est fondamentale pour la satisfaction et le bonheur individuels.

  Perception de la Corruption:
  Une perception élevée de la corruption est associée à un bien-être moindre. La confiance en l'intégrité des institutions publiques et la croyance en une société juste et équitable sont essentielles pour le sentiment de sécurité et de satisfaction au sein d'une population.

  Richesse Économique:
  Il est constaté que les pays avec un PIB par habitant plus élevé tendent à avoir des scores de satisfaction de vie plus élevés. Cela peut refléter la capacité à répondre aux besoins fondamentaux, l'accès à des soins de santé de qualité, et la possibilité d'investir dans l'éducation et les loisirs.

  Propositions pour Augmenter le Ladder Score:

  Renforcer le Support Social:
  Des initiatives pour renforcer les réseaux de soutien social pourraient inclure le développement de programmes communautaires, l'amélioration des systèmes de sécurité sociale, et la création de politiques favorisant l'équilibre travail-vie personnelle.

  Promouvoir la Liberté de Choix:
  Encourager l'autonomie individuelle à travers des réformes législatives qui garantissent les libertés civiles, soutenir l'entrepreneuriat, et offrir une éducation qui valorise la pensée critique peuvent favoriser la liberté de choix.

  Lutter contre la Corruption:
  La mise en œuvre de lois anti-corruption strictes, la promotion de la transparence dans les institutions publiques, et l'éducation à l'éthique civique peuvent réduire la perception de la corruption.

  Stimuler le Développement Économique:
  Investir dans des politiques économiques qui favorisent la croissance, telles que le soutien aux petites et moyennes entreprises, l'innovation technologique, et l'accès à des marchés équitables, peut améliorer le PIB par habitant et, par conséquent, le bien-être général.

  Conclusion:
  L'augmentation du Ladder Score d'un pays dépend d'une approche holistique qui intègre le renforcement du support social, la promotion de la liberté individuelle, la lutte contre la corruption, et le développement économique. Des politiques bien ciblées et des réformes structurelles sont nécessaires pour toucher ces divers aspects du bien-être national et pour impulser une dynamique positive vers un meilleur bien-être pour tous les citoyens.
  """

  st.markdown(f"<div style='text-align: justify; text-justify: inter-word;'>{texte_7}</div>", unsafe_allow_html=True)