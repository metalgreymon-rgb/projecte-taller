#!/bin/bash
# ============================================
# Script de comprovació d'estat dels serveis
# ============================================

ERRORS=0

echo "======================================"
echo " Comprovació de serveis - $(date)"
echo "======================================"

# Comprovar API Flask
echo -n "[API]  http://localhost:5000/vehicles ... "
if curl -s --max-time 5 http://localhost:5000/vehicles > /dev/null; then
    echo "OK ✓"
else
    echo "KO ✗"
    ERRORS=$((ERRORS+1))
fi

# Comprovar Web Nginx
echo -n "[WEB]  http://localhost:8080 ........... "
if curl -s --max-time 5 http://localhost:8080 > /dev/null; then
    echo "OK ✓"
else
    echo "KO ✗"
    ERRORS=$((ERRORS+1))
fi

# Comprovar Base de Dades MariaDB
echo -n "[DB]   MariaDB (taller-db) ............. "
if docker exec taller-db mysqladmin ping -uroot -pexample --silent > /dev/null 2>&1; then
    echo "OK ✓"
else
    echo "KO ✗"
    ERRORS=$((ERRORS+1))
fi

# Resum
echo "--------------------------------------"
if [ $ERRORS -eq 0 ]; then
    echo " Tots els serveis funcionen correctament."
else
    echo " ATENCIÓ: $ERRORS servei(s) amb errors."
fi
echo "======================================"

exit $ERRORS
