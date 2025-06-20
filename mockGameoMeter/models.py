import ast
import json
from django.db import models
from django.urls import reverse ## NEW
from django.contrib.auth.models import User ## NEW
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd

class Profile(models.Model):
  first_name = models.TextField(blank=False)
  last_name = models.TextField(blank=False)
  city = models.TextField(blank=False)
  email_address = models.TextField(blank=False)
  profile_image_url = models.URLField(blank=True)
  #used to store login info for profile user.
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

class GameScores(models.Model):
  '''
  Stores the fake Tomatometer information for each game, as
  well as an ID that will be used to refer to info about the game.
  '''
  id_number = models.IntegerField(blank=False)
  title = models.TextField(blank=False)
  mock_mc = models.FloatField(blank=True)
  all_percent = models.FloatField(blank=True)
  all_rating = models.TextField(blank=True)
  tc_percent = models.FloatField(blank=True)
  tc_rating = models.TextField(blank=True)
  user_percent = models.FloatField(blank=True)
  user_rating = models.TextField(blank=True)
  critics_consensus = models.TextField(blank=True, null=True, max_length=100000)

  # numbers to determine symbol for accompanying ratings.
  all_symbol = models.FloatField(blank=True)
  tc_symbol = models.FloatField(blank=True)
  user_symbol = models.FloatField(blank=True)

  def __str__(self):
    return f'The video game {self.title} is score-ready with ID {self.id_number}.'
  
    
class MetaBars(models.Model):
  """
  Stores the information for the Metascores that will be used to create color bars
  representing the metascores.
  """
  id_number = models.IntegerField(blank=False)
  score_list = models.JSONField(blank=False)

def __str__(self):
  return f'The id number {self.id_number} has a list of metascores {self.score_list}.'

class GameInfo(models.Model):
  '''
  Stores the Rawg Information for each game, as well as an ID that will be 
  used to refer to info about the game.
  '''
  id_number = models.IntegerField(blank=False)
  slug = models.TextField(blank=False)
  name = models.TextField(blank=False)
  release_date = models.DateField(blank=True)
  tba = models.BooleanField(blank=True)
  website = models.URLField(blank=True)
  platforms = models.TextField(blank=True)
  developers = models.TextField(blank=True)
  genres = models.TextField(blank=True)
  publishers = models.TextField(blank=True)
  esrb_rating = models.TextField(blank=True)
  poster_link = models.URLField(blank=True)
  critics_score = models.TextField(blank=True, null=True)

  '''
  id_number = models.IntegerField(blank=False)
  title = models.TextField(blank=False)
  mock_mc = models.FloatField(blank=True, null=True)
  all_percent = models.FloatField(blank=True)
  all_rating = models.TextField(blank=True)
  tc_percent = models.FloatField(blank=True)
  tc_rating = models.TextField(blank=True)
  user_percent = models.FloatField(blank=True)
  user_rating = models.TextField(blank=True)
  critics_consensus = models.TextField(blank=True, null=True)
  '''

  def game_scores(self):
    scores = GameScores.objects.filter(id_number=self.id_number)
    if len(scores) > 0:
      score = scores.first()
      if score.mock_mc is not None:
        score.mock_mc *= 100 
      if score.all_percent is not None:
        score.all_percent *= 100
        r_all = round(score.all_percent,0)
        score.all_percent = r_all
      if score.tc_percent is not None:
        score.tc_percent *= 100 
        r_tc = round(score.tc_percent,0)
        score.tc_percent = r_tc
      if score.user_percent is not None:
        score.user_percent *= 100
        r_user = round(score.user_percent,0)
        score.user_percent = r_user
      return score
    else:
      return None
  
  def bar_length(self):
    metabars = MetaBars.objects.filter(id_number = self.id_number)
    if len(metabars) > 0:
      length = float(len(metabars.first().score_list))
      return 200/length
  
  def meta_bars(self):
    metabars = MetaBars.objects.filter(id_number = self.id_number)
    
    if len(metabars) > 0:
      red_hex = (255,0,0)
      yellow_hex = (255,255,0)
      green_hex = (0,176,80)
      metabar = metabars.first()
      color_list = []
      for value in metabar.score_list:
        
        #print(value)
        if int(value) <= 63:
          ratio = value / 63 
          r = 255
          g = int((red_hex[1]*(1-ratio))+(yellow_hex[1]*(ratio)))
          b = 0
        else:
          ratio = (value-63) / (37) 
          r = int((yellow_hex[0]*(1-ratio))+(green_hex[0]*ratio))
          g = int((yellow_hex[1]*(1-ratio))+(green_hex[1]*ratio))
          b = int((yellow_hex[2]*(1-ratio))+(green_hex[2]*ratio))
        hex_color = f'#{r:02X}{g:02X}{b:02X}'
        color_list.append(hex_color)

      return color_list
    else:
      return None
    

  def __str__(self):
    return f'The video game {self.name} has been added with ID number {self.id_number}.'



def load_info():
  '''
  Load the video game information from a CSV file.
  '''

  # delete all records
  GameInfo.objects.all().delete()

  # open the file for reading one line at a time
  filename = '/Users/DBeye/django_game/media/game_info.csv'
  # open the file for reading
  f = open(filename, encoding="utf8") 
  # discard the first line containing headers
  headers = f.readline()



  # go through the entire file one line at a time
  for line in f:
    
    try:
      #split the CSV file into fields
      fields = line.split(',')

      bool = False
      if fields[4] == "TRUE":
        bool = True

      age_rating = 'RP'
      if fields[10] != '\n':
        age_rating = fields[10]

      GameInfo.objects.filter(id_number=fields[0]).delete()
    

      #create an instance of the GameInfo object
      result = GameInfo(
        id_number = fields[0],
        slug = fields[1],
        name = fields[2],
        release_date = fields[3],
        tba = bool,
        website = fields[5],
        platforms = fields[6],
        developers = fields[7],
        genres = fields[8],
        publishers = fields[9],
        esrb_rating = age_rating,
      )
      result.save()
    except:
      print(f"EXCEPTION OCCURED: {fields}.")

  print("Done.") 



def load_scores():
  '''
  Load the video game scores from a CSV file.
  '''

  # delete all records
  GameScores.objects.all().delete()

  # open the file for reading one line at a time
  filename = '/Users/DBeye/django_game/media/game_scores.csv'
  # open the file for reading
  f = open(filename) 
  # discard the first line containing headers
  headers = f.readline()

  

  # go through the entire file one line at a time
  for line in f:

    try:
      #split the CSV file into fields
      fields = line.split(',')

      all = fields[3]
      #print("ALL IS "+all)
      tc = fields[5]
      #print("TC IS "+tc)

      all_pic = 5.0
      tc_pic = 5.0

      
      if float(all) >= 0.75:
        #print("CERTIFIED FRESH.")
        all_pic = 2
        tc_pic = 2
      elif float(all) <= 0.74 and float(all) >= 0.60 and float(tc) >= 0.60:
        #print("FRESH")
        all_pic = 1
        tc_pic = 1
      elif float(all) <= 0.74 and float(all) >= 0.60 and float(tc) <= 0.59:
        #print("FRESH WITH THE MASSES, NOT WITH THE ELITE")
        all_pic = 1
        tc_pic = 0
      elif float(all) <= 0.59 and float(tc) >= 0.60:
        #print("DISLIKED BY ALL EXCEPT THE ELITE")
        all_pic = 0
        tc_pic = 1
      elif float(all) <= 0.59 and float(tc) <= 0.59:
        #print("UNIVERSALLY DISLIKED")
        all_pic = 0
        tc_pic = 0
      
      user = fields[7]
      user_pic = 2.0
      if float(user) >= 0.6:
        user_pic = 1.0
      else:
        user_pic = 0.0
      


      #create an instance of the GameScores object
      result = GameScores(
        id_number = fields[0],
        title = fields[1],
        mock_mc = fields[2],
        all_percent = fields[3],
        all_rating = fields[4],
        tc_percent = fields[5],
        tc_rating = fields[6],
        user_percent = fields[7],
        user_rating = fields[8],
        all_symbol = all_pic,
        tc_symbol = tc_pic,
        user_symbol = user_pic,
        critics_consensus = fields[9],
      )
      result.save()
      #print("Result saved")

    except:
      print(f"EXCEPTION OCCURED: {fields}.")

  print("Done.") 

# def critics_symbol():
# MyModel.objects.filter(pk=some_value).update(field1='some value')


def make_metabars():
  meta_info = pd.read_csv("/Users/DBeye/django_game/media/meta_lists.csv")

  MetaBars.objects.all().delete()
  len(meta_info)
  for i in range(0,len(meta_info)):
    game = meta_info.iloc[i].copy()
    game_id = game['id']
    game_list = game['s_lists']
    print(game_id)
    
    game_list = json.loads(game_list)
    print(type(game_list))


    results = MetaBars(
      id_number = game_id, 
      score_list = game_list
    )
    print("Results are :",results.score_list)

    results.save()
    """
    """
