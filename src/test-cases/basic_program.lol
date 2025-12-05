BTW if w/o MEBBE, 1 only, everything else is invalid
HOW IZ I menu
	VISIBLE "1. Compute age"
	VISIBLE "2. Compute tip"
	VISIBLE "3. Compute square area"
	VISIBLE "0. Exit"
	VISIBLE "Choice: " !
IF U SAY SO

HAI
	WAZZUP
		I HAS A choice ITZ 1
		I HAS A input
		I HAS A num1 ITZ 0
	BUHBYE
	
	IM IN YR zoop UPPIN YR num1 TIL BOTH SAEM choice AN 0
		I IZ menu MKAY
		GIMMEH choice

		choice
		WTF?
			OMG 1
				VISIBLE "Enter birth year: "
				GIMMEH input
				VISIBLE DIFF OF 2022 AN input
				GTFO
			OMG 2
				VISIBLE "Enter bill cost: "
				GIMMEH input
				VISIBLE "Tip: " + PRODUKT OF input AN 0.1
				GTFO
			OMG 3
				VISIBLE "Enter width: "
				GIMMEH input
				VISIBLE "Square Area: " + PRODUKT OF input AN input
				GTFO
			OMG 0
				VISIBLE "Goodbye"
			OMGWTF
				VISIBLE "Invalid Input!"
		OIC
	IM OUTTA YR zoop

KTHXBYE