// --------------------------------------------- Begin increment_widget namespace -------------------------------------------------
//Copyright (c) 2015 TBillTech.  

//This Source Code Form is subject to the terms of the Mozilla Public
//License, v. 2.0. If a copy of the MPL was not distributed with this
//file, You can obtain one at http://mozilla.org/MPL/2.0/.

var increment_widget = increment_widget = increment_widget || {}

with(increment_widget)
{
    Constructor = function(msg)
    {
        this.HaveWork = HaveWork;
        this.DoWork = DoWork;
	this.Destructor = Destructor;
    };

    HaveWork = function()
    {
	if (this.theElement.hasAttribute('haveWork'))
        {
            return (this.theElement.getAttribute('haveWork') === 'true');
        }
	return false;
    };

    DoWork = function()
    {
        var theElement = this.theElement;
	var theParagraph = theElement.firstChild.firstChild;
	var priorValue = +theElement.getAttribute('currentValue');
	var incrementBy = +theElement.getAttribute('incrementBy');
	theElement.setAttribute('currentValue', 
				(priorValue + incrementBy).toString());
	theParagraph.textContent = theElement.getAttribute('currentValue');
	if(this.HaveListener('increment'))
        {
            var event = this.CreateEvent();
            event.detail = 'done';
            this.SendEvent(event, 'increment');
        };
        this.theElement.setAttribute('haveWork', 'false');
    };

    Destructor = function()
    {
	var theElement = this.theElement;
	var theParent = theElement.parentNode;
	theParent.setAttribute('incrementor_destroyed', 'true');
    };

    with(domsocket)
    {
        SetWidgetClass('IncrementWidget', Constructor);
    }
};
// --------------------------------------------- end increment_widget namespace -------------------------------------------------
