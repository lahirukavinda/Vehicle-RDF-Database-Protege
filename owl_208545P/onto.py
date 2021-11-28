import os
import sys

import pyparsing
import rdflib
from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, validators

from owlready2 import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

rdf_filename = "misc/vehicle_5.rdf"

class ReusableForm(Form):
    query = StringField('Query:', validators=[validators.data_required()])

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        global graph
        form = ReusableForm(request.form)
        if form.errors:
            print(form.errors)

        base_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.usa-vehicles/ontologies/vehicles#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"""

        output = {}
        query = ''
        filter = False

        if request.method == 'POST':

            if(request.form['but1']=='toyota'):
                query = '''SELECT ?Vehicle ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?Vehicle rdf:type owl:NamedIndividual.
                    ?Vehicle :hasManufacturer ?Company.
                    ?Company :hasRegionName "Toyota-USA".
                    ?Vehicle :hasPriceValue ?Price.
                    ?Vehicle :hasCombinedMPGValue ?MPG.
                    ?Vehicle :hasManufacturedYear ?Year.
                    ?Vehicle :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='volk'):
                query = '''SELECT ?Vehicle ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?Vehicle rdf:type owl:NamedIndividual.
                    ?Vehicle :hasManufacturer ?Company.
                    ?Company :hasRegionName "Volksvagan-USA".
                    ?Vehicle :hasPriceValue ?Price.
                    ?Vehicle :hasCombinedMPGValue ?MPG.
                    ?Vehicle :hasManufacturedYear ?Year.
                    ?Vehicle :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='ford'):
                query = '''SELECT ?Vehicle ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?Vehicle rdf:type owl:NamedIndividual.
                    ?Vehicle :hasManufacturer ?Company.
                    ?Company :hasRegionName "Ford-USA".
                    ?Vehicle :hasPriceValue ?Price.
                    ?Vehicle :hasCombinedMPGValue ?MPG.
                    ?Vehicle :hasManufacturedYear ?Year.
                    ?Vehicle :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='honda'):
                query = '''SELECT ?Vehicle ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?Vehicle rdf:type owl:NamedIndividual.
                    ?Vehicle :hasManufacturer ?Company.
                    ?Company :hasRegionName "Honda-USA".
                    ?Vehicle :hasPriceValue ?Price.
                    ?Vehicle :hasCombinedMPGValue ?MPG.
                    ?Vehicle :hasManufacturedYear ?Year.
                    ?Vehicle :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='nissan'):
                query = '''SELECT ?Vehicle ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?Vehicle rdf:type owl:NamedIndividual.
                    ?Vehicle :hasManufacturer ?Company.
                    ?Company :hasRegionName "Nissan-USA".
                    ?Vehicle :hasPriceValue ?Price.
                    ?Vehicle :hasCombinedMPGValue ?MPG.
                    ?Vehicle :hasManufacturedYear ?Year.
                    ?Vehicle :hasSeatingValue ?Seat.
                }'''

            elif(request.form['but1']=='cars'):
                query = '''SELECT ?Cars ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?Cars rdf:type :Cars.
                    ?Cars :hasPriceValue ?Price.
                    ?Cars :hasCombinedMPGValue ?MPG.
                    ?Cars :hasManufacturedYear ?Year.
                    ?Cars :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='suv'):
                query = '''SELECT ?SUVorCrossOver ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?SUVorCrossOver rdf:type :SUVs.
                    ?SUVorCrossOver :hasPriceValue ?Price.
                    ?SUVorCrossOver :hasCombinedMPGValue ?MPG.
                    ?SUVorCrossOver :hasManufacturedYear ?Year.
                    ?SUVorCrossOver :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='elec'):
                query = '''SELECT ?ElectricCars ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?ElectricCars rdf:type :ElectricCars.
                    ?ElectricCars :hasPriceValue ?Price.
                    ?ElectricCars :hasCombinedMPGValue ?MPG.
                    ?ElectricCars :hasManufacturedYear ?Year.
                    ?ElectricCars :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='truck'):
                query = '''SELECT ?TruckOrPickup ?Price ?MPG ?Year ?Seat 
                WHERE { 
                    ?TruckOrPickup rdf:type :Trucks.
                    ?TruckOrPickup :hasPriceValue ?Price.
                    ?TruckOrPickup :hasCombinedMPGValue ?MPG.
                    ?TruckOrPickup :hasManufacturedYear ?Year.
                    ?TruckOrPickup :hasSeatingValue ?Seat.
                }'''
            elif(request.form['but1']=='all'):
                query = '''SELECT ?Vehicle ?Price ?MPG ?Year ?Seat 
                WHERE {
                    ?Vehicle rdf:type owl:NamedIndividual.
                    ?Vehicle :hasPriceValue ?Price.
                    ?Vehicle :hasCombinedMPGValue ?MPG.
                    ?Vehicle :hasManufacturedYear ?Year.
                    ?Vehicle :hasSeatingValue ?Seat.
                }'''

            else:
                price = request.form['query']
                filter = True
                query = '''SELECT ?Vehicle ?Price
                WHERE {
                    ?Vehicle rdf:type owl:NamedIndividual.
                    ?Vehicle :hasPriceValue ?Price.
                }'''
                print(price)
                print(type(price))
            
            print("\n",type(query))
            print (".......",query,"............")
            cols = query.split('WHERE')[0].split()
            cols = [s.strip('?') for s in cols if s.startswith('?')]

            query = base_query + query

        try:
            results = graph.query(query)
            
            data = []
            for s in results:
                if not any(isinstance(x, rdflib.term.BNode) for x in s):
                    temp = []
                    for x in s:
                        if isinstance(x,rdflib.term.Literal):
                            if(filter):
                                if(x > price):
                                    temp = []
                                    break
                            temp.append(x)
                        else:
                            temp.append(x.replace(x.defrag() + "#", ''))
                    if temp : 
                        data.append(temp)
                    #print([isinstance(x,rdflib.term.URIRef) for x in s])
                    

            output = {'columns': cols,
                      'data': data}

            flash('Results ready!')
        except pyparsing.ParseException:
            print("ERROR: query entered...\n", query)
            flash('Error: Invald Query')

        return render_template('home.html', form=form, title="Vehicle Price Database", output=output)


if __name__ == "__main__":
    if not os.path.isfile(rdf_filename):
        print(f"RDF file '{rdf_filename}' not found")
        sys.exit(1)

    onto = get_ontology(rdf_filename).load()
    graph = default_world.as_rdflib_graph()

    app.run(debug=True)
