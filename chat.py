from openai import OpenAI
from chiave import KEY
import json

from semaphores import wait_semaphore, set_semaphore, clear_semaphores
import sys


if len(sys.argv) < 3:
    print("Uso: python script.py nome_file_output.txt")
    sys.exit(1)

print(sys.argv)

OUTPUT_FOLDER= sys.argv[1]

client = OpenAI(api_key=KEY)

risposte = []


for i in range (4):
  transcription_fname = OUTPUT_FOLDER + "/" + str(i+1) + ".txt"
  print(i)

  with open(transcription_fname) as f:
    risposte.append(f.read())


#risp1="Vado solitamente al mercato"
#risp2="Una volta al mese"
#risp3="Prendo sempre quello che c'è in offerta"
#risp4="Non mi frega molto"

client = OpenAI(api_key=KEY)

print("fino a qui ok")

response = client.responses.create(
  model="gpt-4.1",
  input=[
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "Sei un assistente intelligente che stabilisce a quale profilo corrisponde l'utente\n1) San Narciso Patrono degli Specchi (livello di sostenibilità: 1 su 4) \n- non mostra interesse per la sostenibilità o l’etica;\n- è fortemente orientato all’estetica, al brand, all’apparenza;\n- predilige l’originalità o la moda rispetto al rispetto ambientale.;\n- frasi chiave: “Basta che stia bene addosso”, “Non mi importa se è fast fashion”, “L’importante è avere stile”. \nparole con priorità maggiore: shein, temu, aliexpress, wish.\n\n2) Santa Saveria da Genova (livello sostenibilità: 2 su 4)\n- fa scelte in base al risparmio, senza troppe riflessioni su etica o estetica;\n- è sensibile alle promozioni, agli sconti, agli outlet;\n- predilige l’acquisto impulsivo quando trova un affare.\n- frasi chiave: “L’ho preso al 70% di sconto!”, “Per quel prezzo non potevo lasciarlo lì”, “Compro solo quando c’è l'offerta.\n \n3) Beata Vergine delle Reliquie (livello sostenibilità: 3 su 4)\n- pianifica i suoi acquisti, ricerca alternative originali, spesso second-hand o artigianali.\n- unisce estetica e sostenibilità.\n- ha piacere a raccontare le storie dietro agli oggetti che acquista.\n- frasi chiave: “L’ho trovato in un mercatino!”, “Non compro spesso, ma scelgo bene”, “Era usato ma perfetto per me”.\n\n4) San Girolamo Protettore dei Perduti (livello sostenibilità: 4 su 4)\n- è intransigente riguardo alla sostenibilità;\n- giudica apertamente le scelte poco etiche degli altri;\n- sceglie solo materiali naturali, etici, spesso rinuncia a comprare del tutto;\n- frasi chiave: “non compro più vestiti”, non capisco come si possa ancora comprare fast fashion”, “La sostenibilità viene prima di tutto”.\n\nquando l'utente risponde \"valuta\" , valuta le risposte e in base alle risposte dell'utente, ritorna solo il numero di profilo corrispondente, senza commenti e analisi "
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Quando senti il bisogno di rinnovare il tuo guardaroba, dove ti rechi di solito per trovare ciò che cerchi?"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": risposte[0]
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Quanto spesso decidi di aggiungere nuovi vestiti alla tua vita e quali motivazioni, sia pratiche che interiori, ti guidano in queste scelte?"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": risposte[1]
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Quando scegli un nuovo capo d’abbigliamento, quali sono gli aspetti che per te contano di più? Prediligi il prezzo e le offerte migliori o magari tieni d’occhio la qualità o l’origine dei materiali di cui è composto?"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": risposte[2]
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "E quando vedi o senti qualcuno che fa acquisti sconsiderati da grandi aziende del fast fashion, come reagisci?"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": risposte[3]
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "valuta"
        }
      ]
    }
  ],
  text={
    "format": {
      "type": "text"
    }
  },
  reasoning={},
  tools=[],
  temperature=1,
  max_output_tokens=2048,
  top_p=1,
  store=True
)
#print(response.choices[0].message.content)

print("qui dopo la valutazione ok")

#TODO se non è numerico forzare a 1
print(response.output_text)
NUMSANTINO=response.output_text
#NUMSANTINO=1


result_fname =  OUTPUT_FOLDER + "/" + "numsantino" + ".txt"

# Salva la trascrizione in un file .txt
with open(result_fname, "w", encoding="utf-8") as f:
    f.write(str(NUMSANTINO))

print("Salvato in" + result_fname)

set_semaphore("chat")

#output_folder/ con file txt con il numero dell'utente risultato

#Response(id='resp_681b61cb0c748191907db5b4bc2d4fdc07e9284e14ec6a65', created_at=1746624971.0, error=None, incomplete_details=None, instructions=None, metadata={}, model='gpt-4.1-2025-04-14', object='response', output=[ResponseOutputMessage(id='msg_681b61cb9710819186870c1f718ec17707e9284e14ec6a65', content=[ResponseOutputText(annotations=[], text='2', type='output_text')], role='assistant', status='completed', type='message')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[], top_p=1.0, max_output_tokens=2048, previous_response_id=None, reasoning=Reasoning(effort=None, generate_summary=None, summary=None), service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text')), truncation='disabled', usage=ResponseUsage(input_tokens=725, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=2, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=727), user=None, store=True)