from django.shortcuts import render
from django.http import Http404  
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from numpy import random
import markdown2




class SearchForm(forms.Form):
	search = forms.CharField(label = "Nueva Busqueda")

class newEntryTitle(forms.Form):
	title = forms.CharField(label = "Título")

class EditPage(forms.Form):
	content = forms.CharField(widget = forms.Textarea)


# View for index. Get all entries in a list.
def index(request):
	if request.method == "GET":
		    return render(request, "encyclopedia/index.html", {
		        "entries": util.list_entries(), "form": SearchForm()
		    })


# EntryPage 
def entrypage(request, entry):
	if request.method == "POST":
		print("milanesa")
		if util.get_entry(entry):
			titles = str(entry)
			entrie = str(util.get_entry(entry))
			print(titles, entrie)	
			return render(request, "encyclopedia/entrypage.html", {
				titles: "entry", entrie: "sasa"
				})

		else:
			raise Http404("No existe entrada")



	else:
		print("olaf el vikingo")
		if util.get_entry(entry):
			titles = str(entry)
			entrie = str(util.get_entry(entry))
			entrie = markdown2.markdown(entrie)
			print(titles)
			return render(request, "encyclopedia/entrypage.html", { "titles":titles, "entrie":entrie, "form": SearchForm()})

		raise Http404("Estamos en construcción :)")



#  Agregando 31/1/21
def search(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			busqueda = form.cleaned_data["search"]
			busqueda = busqueda.casefold()
			title = str(busqueda)
			entry = util.get_entry(title)
			if entry is not None:
				return render(request, "encyclopedia/entrypage.html", {
					"entry": entry, "title": title, "form": SearchForm()
					})

			else:
				abc = []
				for entrada in util.list_entries():
					absec = str(entrada).casefold()
					if title in absec:
						abc.append(entrada)
						print(abc)

				print(f"esta es la lista:{abc}")
				return render(request, "encyclopedia/search.html", {
					"abc": abc
					})


		else:
	 	   return render(request, "encyclopedia/layout.html", {
	    	"form": SearchForm()
	    	})

	else:
	 	   return render(request, "encyclopedia/layout.html", {
	    	"form": SearchForm()
	    	})


def newpage(request):
	if request.method == "POST":
		form = newEntryTitle(request.POST)
		if form.is_valid():
			title = str(form.cleaned_data["title"])
			print("title")
			contenido = str(request.POST.get("contenido"))
			print(contenido)
			entry = util.get_entry(title)
			if entry is not None:
				raise Http404("La entrada que está intentando agregar ya existe.")

				#raise Http404("En construcción")

			else:
				util.save_entry(title, contenido)
				contenido = markdown2.markdown(contenido)
				return render(request, "encyclopedia/entrypage.html", {
					"titles":title, "entrie":contenido, "form":SearchForm()
					})



		else:
			return render(request, "encyclopedia/newpage.html", {
				"newtitle": newEntryTitle(), "form": SearchForm()
				})

	else:
		return render(request, "encyclopedia/newpage.html", {
			"newtitle": newEntryTitle(), "form": SearchForm()
			})


def editpage(request):
	form = EditPage()
	title = str(request.POST.get("editvientre"))
	title = (title[5:])
	contenido = util.get_entry(title)
	print(f"eeste es el titulo : {title}")

	if request.method == "POST":
		if form.is_valid():
			title = str(form.cleaned_data["title"])
			print("tintin")
			contenido = str(form.cleaned_data["title"])
			util.save_entry(title, contenido)
			contenido = markdown2.markdown(contenido)
			return HttpResponseRedirect("encyclopedia/entrypage.html", {
					"title": title, "entry": contenido
					})

		else:	
			#title = str(request.POST.get("entry"))
			contenido = util.get_entry(title)
			print("neeeeerf")
			print(contenido)

			data = {'content': contenido}
			form2 = EditPage(data)
			print(form2.is_bound)

			return render(request, "encyclopedia/editpage.html", {
					"title": title, "editform": form2, "form": SearchForm()
					})


	# Parece que no se llegaría a esta view al menos que tipeemos directamente en la barra de direcciones.
	else:
		return render(request, "encyclopedia/index.html", {
				"entries": util.list_entries(), "form":SearchForm()
				})



def savedpage(request):
	if request.method == "POST":
		form = EditPage(request.POST)
		if form.is_valid():
			title = str(request.POST.get("viejachonga"))
			title = (title[5:])
			contenido = form.cleaned_data["content"]
			util.save_entry(title, contenido)
			contenido = markdown2.markdown(contenido)
			return render(request, "encyclopedia/entrypage.html", {
				"titles": title, "entrie": contenido, "form":SearchForm()
				})


		else:
			raise Http404("estamos en construcción")

	else:
		raise Http404("En Construcción")

def randompage(request):

	# La solicitud POST parece que no serviría en este caso
	if request.method == "POST":
		x = random.rand()
		x = x * 100
		allentries = util.list_entries()
		print(f"x es {x} y todas las entradas son las siguientes: {allentries}")
		raise Http404("Estamos construyendo randompage en POST method")

	else:
		# En la primera parte de este código describo una función random con defectos
		x = random.rand()
		x = int(x * 100)
		allentries = util.list_entries()
		sas = int(x / len(allentries))
		print(f"x es {x} y sas es{sas} y todas las entradas son las siguientes: {allentries}")
		print(f"esta es la entrada 0: {allentries[0]}")

		# En esta segunda parte del código describo una función random más efectiva
		contenedor = []
		for i in range(len(allentries)):
			contenedor.append(i)

		contenedor2 = []
		for m in range(len(allentries)):
			m = 1/(len(allentries))
			contenedor2.append(m)

		toke = random.choice(contenedor, p=contenedor2 , size=(1))
		toke = int(toke)
		print(f"contenedor: {contenedor}")
		print(f"contenedor2: {contenedor2}")
		print(f"toke:{toke}")
		title = allentries[toke]
		entrie = markdown2.markdown(util.get_entry(title))

		return render(request, "encyclopedia/entrypage.html", {
			"titles": title, "entrie": entrie, "form": SearchForm()
			})
		
#		raise Http404("Estamos construyendo randompage en GET method de solicitud")

"""
		title = "Agregar formula para obtener título"
		return render(request, "encyclopedia/entripage.html" {
			"titles": title, "entrie": util.get_entry(title), "form":SearchForm()
			})
"""