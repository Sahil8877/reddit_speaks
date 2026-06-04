import os,sys
import time
import requests
import base64
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
import ollama
from moviepy import ImageSequenceClip, ImageClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioClip,AudioFileClip, concatenate_audioclips, concatenate_videoclips
import textwrap
from datetime import datetime
