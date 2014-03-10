#!/usr/bin/env python

import xml.etree.ElementTree as ET
import csv

def remove_namespace(doc, namespace):
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

with open(r"/home/dth/IDEA Projects/VorTidsMusik/VorTidsMusik.xml", 'r') as infile:
    tree = ET.ElementTree(file=infile)
    root = tree.getroot()
    remove_namespace(tree, 'http://www.loc.gov/MARC21/slim')

    for record in root:
        idForFile = ""
        PBCoreDescriptionDocument = ET.Element("PBCoreDescriptionDocument")
        PBCoreDescriptionDocument.set("xlmns", "http://www.pbcore.org/PBCore/PBCoreNamespace.html")
        PBCoreDescriptionDocument.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        PBCoreDescriptionDocument.set("xsi:schemaLocation", "http://www.pbcore.org/xsd/pbcore-1.3.xsd")

        PBCoreAssetType = ET.SubElement(PBCoreDescriptionDocument, "pbcoreAssetType")
        PBCoreAssetType.set("source", "PBCore AssetType Picklist")
        PBCoreAssetType.text = "Program"

        for datatype in record.iterfind('./datafield[@tag="440"]'):
            idText = ""
            for id in datatype.iterfind('subfield[@code="v"]'):
                idText = id.text
                idForFile = id.text
            PBCoreIdentifier = ET.SubElement(PBCoreDescriptionDocument, "pbcoreIdentifier")
            Identifier = ET.SubElement(PBCoreIdentifier, "identifier")
            Identifier.text = idText
            IdentifierSource = ET.SubElement(PBCoreIdentifier, "identifierSource")
            IdentifierSource.text = "Statsbiblioteket. Vor tids musik"

        for datatype in record.iterfind('./datafield[@tag="245"]'):
            titleText = ""
            for title in datatype.iterfind('subfield[@code="a"]'):
                titleText = title.text

            PBCoreTitle = ET.SubElement(PBCoreDescriptionDocument, "pbcoreTitle")
            Title = ET.SubElement(PBCoreTitle,"title")
            Title.text = titleText

            TitleType = ET.SubElement(PBCoreTitle, "titleType")
            TitleType.text = "Program"
            TitleType.set("source", "PBCore TitleType Picklist")

        PBCoreTitle = ET.SubElement(PBCoreDescriptionDocument, "pbcoreTitle")
        Title = ET.SubElement(PBCoreTitle,"title")
        Title.text = "Vor Tids Musik"
        TitleType = ET.SubElement(PBCoreTitle, "titleType")
        TitleType.text = "series"
        TitleType.set("source","PBCore TitleType Picklist")

        for datatype in record.iterfind('./datafield[@tag="245"]'):
            descriptionText = ""
            for description in datatype.iterfind('subfield[@code="c"]'):
                descriptionText = description.text
        PBCoreDescription = ET.SubElement(PBCoreDescriptionDocument, "pbcoreDescription")
        Description = ET.SubElement(PBCoreDescription, "description")
        Description.text = descriptionText
        DescriptionType = ET.SubElement(PBCoreDescription, "descriptionType")
        DescriptionType.text = "langomtale1"
        DescriptionType.set("source", "PBCore DescriptionType Picklist")

        for datatype in record.iterfind('./datafield[@tag="245"]'):
            descriptionText = ""
            for description in datatype.iterfind('subfield[@code="e"]'):
                descriptionText = description.text
        PBCoreDescription = ET.SubElement(PBCoreDescriptionDocument, "pbcoreDescription")
        Description = ET.SubElement(PBCoreDescription, "description")
        Description.text = descriptionText
        DescriptionType = ET.SubElement(PBCoreDescription, "descriptionType")
        DescriptionType.text = "kortomtale"
        DescriptionType.set("source", "PBCore DescriptionType Picklist")

        for datatype in record.iterfind('./datafield[@tag="700"]'):
            firstnameText = ""
            surnameText = ""
            yearText = ""
            for firstname in datatype.iterfind('subfield[@code="h"]'):
                firstnameText = firstname.text
            for surname in datatype.iterfind('subfield[@code="a"]'):
                surnameText = surname.text
            for year in datatype.iterfind('subfield[@code="c"]'):
                yearText = ", "+year.text
            PBCoreContributor = ET.SubElement(PBCoreDescriptionDocument, "pbcoreContributor")
            Contributor = ET.SubElement(PBCoreContributor, "contributor")
            Contributor.text = firstnameText+" "+surnameText+yearText
            ContributorRole = ET.SubElement(PBCoreContributor, "contributorRole")
            ContributorRole.set("source", "PBCore DescriptionType Picklist")
            ContributorRole.text = "contributor"
        for datatype in record.iterfind('./datafield[@tag="710"]'):
            bandText = ""
            for bandname in datatype.iterfind('subfield[@code="a"]'):
                bandText = bandname.text
            PBCoreContributor = ET.SubElement(PBCoreDescriptionDocument, "PBCoreContributor")
            Contributor = ET.SubElement(PBCoreContributor, "contributor")
            Contributor.text = bandText
            ContributorRole = ET.SubElement(PBCoreContributor, "contributorRole")
            ContributorRole.set("source", "PBCore DescriptionType Picklist")
            ContributorRole.text = "contributor"

        PBCoreGenre = ET.SubElement(PBCoreDescriptionDocument, "pbcoreGenre")

        Genre = ET.SubElement(PBCoreGenre, "genre")
        Genre.text = "Radio"


        kanalnavn = ""
        findesIkke = ""
        with open('/home/dth/IDEA Projects/VorTidsMusik/kanalnavne.csv', 'rb') as f:
                    reader = csv.reader(f)
                    rownum = 0
                    for row in reader:
                        if rownum == 0:
                            header = row
                        else:
                            if row[0] == idForFile:
                                print "id: "+idForFile
                                kanalnavn = (row[3]).encode("utf-8")
                                findesIkke = (row[4]).decode("utf-8")
                        rownum += 1

        for datatype in record.iterfind('./datafield[@tag="260"]'):
            publisherText = ""
            for publisher in datatype.iterfind('subfield[@code="b"]'):
                if kanalnavn == "":
                    publisherText = publisher.text
                else:
                    publisherText = publisher.text+" "+kanalnavn
            PBCorePublisher = ET.SubElement(PBCoreDescriptionDocument, "pbcorePublisher")
            Publisher = ET.SubElement(PBCorePublisher, "publisher")
            Publisher.text = publisherText
            PublisherRole = ET.SubElement(PBCorePublisher, "publisherRole")
            PublisherRole.set("source","PBCore PublisherRole Picklist")
            PublisherRole.text = "Distributor"

        PBCoreInstantiation = ET.SubElement(PBCoreDescriptionDocument, "pbcoreInstantiation")

        for datatype in record.iterfind('./datafield[@tag="440"]'):
            identifierText = ""
            for identifier in datatype.iterfind('subfield[@code="v"]'):
                identifierText = identifier.text
            PBCoreFormatID = ET.SubElement(PBCoreInstantiation, "pbcoreFormatID")
            FormatIdentifier = ET.SubElement(PBCoreFormatID, "formatIdentifier")
            FormatIdentifier.text = identifierText
            FormatIdentifierSource = ET.SubElement(PBCoreFormatID, "formatIdentifierSource")
            FormatIdentifierSource.text = "Statsbiblioteket. Vor tids musik"
            DateIssued = ET.SubElement(PBCoreInstantiation, "dateIssued")
            if identifierText == "000927" or identifierText == "010128":
                year = "20"+identifierText[0:2]
            else:
                year = "19"+identifierText[0:2]
            month = identifierText[2:4]
            day = identifierText[4:6]
            completeDate = year+"-"+month+"-"+day
            DateIssued.text = completeDate
            FormatLocation = ET.SubElement(PBCoreInstantiation, "formatLocation")
            FormatMediaType = ET.SubElement(PBCoreInstantiation, "formatMediaType")
            FormatMediaType.text = "Sound"
            PBCoreDateAvaliable = ET.SubElement(PBCoreInstantiation, "pbcoreDateAvaliable")
            DateAvaliableStart = ET.SubElement(PBCoreDateAvaliable, "dateAvaliableStart")
            DateAvaliableStart.text = completeDate
            DateAvaliableEnd = ET.SubElement(PBCoreDateAvaliable, "dateAvaliableEnd")
            DateAvaliableEnd.text = completeDate

        PBCoreAnnotation = ET.SubElement(PBCoreDescriptionDocument, "pbcoreAnnotation")
        Annotation = ET.SubElement(PBCoreAnnotation, "annotation")
       
        Annotation.text = findesIkke
        
        tree = ET.ElementTree(PBCoreDescriptionDocument)
        indent(PBCoreDescriptionDocument)
        tree.write("/home/dth/IDEA Projects/VorTidsMusik/output/"+idForFile+".xml", xml_declaration = True, method = "xml", encoding = "UTF-8")
