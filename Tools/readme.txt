architecture:

Program:
    input:
        mouse
        keyboard


    settings:
        GUI:
            size
            position
            no.
        
        tools:
            brush: size, colour
        

    
    GUI:
        toolbar
        viewport:
            canvas:
                set pixel
                set area
                get pixel
                get area
            display:


    #tools will be wrapper for parts around program
    tools:
        brush -> canvas.setpixel(settings.tools.brush
        bucket
        cursor
        eraser
        select
        picker
    
