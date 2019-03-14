# -*- coding: ISO-8859-1 -*-
from skore_api import Skore
import json
from meya import Component
from meya.cards import List, Element, Button

class GetMaterialsList(Component):

    def start(self):

        tokenInfo = self.db.bot.get("skore_token")

        SkoreCreationParams = {
            "email" : self.db.bot.settings["skore_user"], 
			"password" : self.db.bot.settings["skore_key"]
        }
        
        print("THIS IS THE TOKEN INFO,", tokenInfo)
        
        # If token still valid, then use it to avoid re-login
        if tokenInfo and Skore.tokenValid(tokenInfo["expiration"]):
            SkoreCreationParams.update({"token": tokenInfo["token"]})

        skore = Skore(**SkoreCreationParams)

        contents = skore.getSpaceContents("34137")
        if not contents:
            # Possivelmente criar função para adicionar usuário no espaço e enviar login via chat
            text = "I didn't manage to load the materials.\nTry again later or access the materials link directly, using your login provided, here: \nhttp://hiring.skore.io/categories/34137-about-skore/"
            speech = "<speak>I didn't manage to load the materials.Try again later or access the materials link directly, using your login provided, here: <say-as interpret-as=\"verbatim\">http://</say-as>hiring<say-as interpret-as=\"verbatim\">.</say-as>skore<say-as interpret-as=\"verbatim\">.io/</say-as>categories<say-as interpret-as=\"verbatim\">/34137-</say-as>about<say-as interpret-as=\"verbatim\">-</say-as>skore</speak>"
            message = self.create_message(text = text, speech = speech)
        else:
            contentsName = [content["name"] for content in contents["results"]]
            text = "\n".join(["- {}".format(content) for content in contentsName])
            speech = "<speech>" + ", ".join([content for content in contentsName]) + ".</speech>"

            message = self.create_message(text = text, speech = speech)

        return self.respond(message = message, action = "next")