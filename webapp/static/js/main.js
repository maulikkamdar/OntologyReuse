output = [];
ontologyList = [];
typeList = []
typeList["0Ex"] = "Precise Match";
typeList["1AA"] = "Degree 1: Preferred Label - Preferred Label Matching";
typeList["1AE"] = "Degree 1: Preferred Label - Exact Synonym Matching";
typeList["1AR"] = "Degree 1: Preferred Label - Related Synonym Matching";
typeList["1AU"] = "Degree 1: Preferred Label - Other Synonym Matching";
typeList["1EE"] = "Degree 1: Exact Synonym - Exact Synonym Matching";
typeList["1ER"] = "Degree 1: Exact Synonym - Related Synonym Matching";
typeList["1EU"] = "Degree 1: Exact Synonym - Other Synonym Matching";
typeList["1RR"] = "Degree 1: Related Synonym - Related Synonym Matching";
typeList["1RU"] = "Degree 1: Related Synonym - Other Synonym Matching";
typeList["1UU"] = "Degree 1: Other Synonym - Other Synonym Matching";
typeList["2AA"] = "Degree 2: Preferred Label - Intermediate Node - Preferred Label Matching";
typeList["2AE"] = "Degree 2: Preferred Label - Intermediate Node - Exact Synonym Matching";
typeList["2AR"] = "Degree 2: Preferred Label - Intermediate Node - Related Synonym Matching";
typeList["2AU"] = "Degree 2: Preferred Label - Intermediate Node - Other Synonym Matching";
typeList["2EE"] = "Degree 2: Exact Synonym - Intermediate Node - Exact Synonym Matching";
typeList["2ER"] = "Degree 2: Exact Synonym - Intermediate Node - Related Synonym Matching";
typeList["2EU"] = "Degree 2: Exact Synonym - Intermediate Node - Other Synonym Matching";
typeList["2RR"] = "Degree 2: Related Synonym - Intermediate Node - Related Synonym Matching";
typeList["2RU"] = "Degree 2: Related Synonym - Intermediate Node - Other Synonym Matching";
typeList["2UU"] = "Degree 2: Other Synonym - Intermediate Node - Other Synonym Matching";

d3.json("../static/ontologyDescriptions.json", function(response){
    ontologyDescriptions = response["results"]["bindings"];
    for (k in ontologyDescriptions) {
        ontologyList[ontologyDescriptions[k]["acr"]["value"]] = ontologyDescriptions[k]["name"]["value"];
    }
    console.log(ontologyList);
});



function printTable(type) {
    if(output[type].length > 0)
        jQuery('#outputTable tr:last').after('<tr style="border-bottom:1px solid black; background-color:#cccccc"><th colspan="6">'+typeList[type]+'</th></tr>');
    for (k in output[type]) {
        iris = output[type][k]["compositeParams"][0];
        ontologies = output[type][k]["compositeParams"][1].split(":-:");
        newOntologies = [];
        for (m in ontologies) {
            newOntologies.push("<a href='http://bioportal.bioontology.org/ontologies/"+ontologies[m]+"' target='_blank'>" + (typeof ontologyList[ontologies[m]] === "undefined"? ontologies[m] : ontologyList[ontologies[m]]) + "</a>")
        }
        labels = output[type][k]["compositeParams"][2].split(":-:").join(", ");
        var exact = "", related = "", other = "";
        if (output[type][k]["compositeParams"].length > 3) exact = output[type][k]["compositeParams"][3].split(":-:").join(", ");
        if (output[type][k]["compositeParams"].length > 4) related = output[type][k]["compositeParams"][4].split(":-:").join(", ");
        if (output[type][k]["compositeParams"].length > 5) other = output[type][k]["compositeParams"][5].split(":-:").join(", ");
        jQuery('#outputTable tr:last').after('<tr style="border-bottom:1px solid black"><td><a href="' + iris + '" target="_blank">' + iris + '</a></td><td>' + newOntologies.join("<br>") + '</td><td>' + labels + '</td><td>' + exact + '</td><td>' + related + '</td><td>' + other + '</td></tr>');
    }
}

jQuery('#btnCheck').click(function() {
    jQuery.ajax({
        url: '/similarTerms',
        data: jQuery('#formSim').serialize(),
        type: 'POST',
        success: function(response) {
            jQuery('#outputTable').html('<tr><th width="16%">IRI</th><th width="16%">Ontologies</th><th width="16%">Labels</th><th width="18%">Exact Synonyms</th><th width="17%">Related Synonyms</th><th width="17%">Other Synonymns</th></tr>');
            output = JSON.parse(response);
            printTable("0Ex");
            printTable("1AA");
            printTable("1AE");
            printTable("1AR");
            printTable("1AU");
            printTable("1EE");
            printTable("1ER");
            printTable("1EU");
            printTable("1RR");
            printTable("1RU");
            printTable("1UU");
        },
        error: function(error) {
            console.log(error);
        }
    });
});

jQuery("#termString").keydown(function(event) {
    if (event.which == 13){  // enter
      loginUser();
    }
  });