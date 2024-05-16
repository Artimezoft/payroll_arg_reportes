# ¿Cómo publicar una nueva versión en PyPI?

Hay un GitHub action en .github/workflows/python-publish.yml que al haber un nuevo release en el repositorio,
se encarga de publicar la nueva versión en PyPI.  

Para que esto funcione es necesario que este cargado el secret PYPI_API_TOKEN en este repositorio.  

## ¿Cómo se hace un nuevo release?

Los releases se pueden crear desde los tags. Ese es el metodo que usamos.  
La version `0.0.18` se creo así. Se hizo el tag y con este tag se creo un nuevo release.  
Luego de esto se lanzo automáticamente el GitHub action que se encargo de publicar la nueva versión en PyPI.  
