
!
! BASICS

! Automatic Dockerization
! Fortran example

! Prints "Hello world"
!


program hello_world
    
    open(1, file = 'hw.txt', status = 'new')
    write (1,*) "Hello World"
    close(1) 

end program hello_world
