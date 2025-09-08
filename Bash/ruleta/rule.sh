#!/bin/bash

# * Colours
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"

#!Funcion Ctrl + C 
function ctrl_c(){ 
  echo -e "${redColour}\n\n[!] SALIENDO...${endColour}" 
  tput cnorm && exit 1 
}

#* Panel de Ayuda
function helpPanel(){
  echo -e "\n${yellowColour}[+]${endColour}${grayColour}Uso:${endColour} ${blueColour}$0${endColour}\n"
  echo -e "\t${blueColour}-m${endColour}${grayColour} Dinero con el que se desea jugar${endColour}"
  echo -e "\t${blueColour}-t${endColour}${grayColour} Técnica que se desea aplicar${endColour} ${blueColour}(martingala / LabouchereInversa(Poner exactamente así para que no de error))${endColour}\n"
  exit 1
}

#!Martingala
function martingala(){
  echo -e "\n${yellowColour}[+]${endColour}${grayColour} Tu dinero actual es:${endColour} ${blueColour}$money$ ${endColour}"
  echo -ne "${yellowColour}[+]${endColour}${grayColour} Cuanto dinero piensa apostar?${endColour}${yellowColour} --> ${endColour}" && read initial_bet
  echo -ne "${yellowColour}[+]${endColour}${grayColour} A que desea apostar continuamente (par/impar)?${endColour}${yellowColour} -->${endColour} " && read par_impar
  echo -e "${yellowColour}[+]${endColour} ${grayColour}Vamos a jugar con una cantidad inicial de${endColour}${blueColour} $initial_bet$ ${endColour}${grayColour} a${endColour} ${blueColour}$par_impar${endColour}"

  backup_initial_bet=$initial_bet
  play_counter=1
  jugadas_malas=""
  mayor_dinero=$money
  tput civis 
  while true; do
    money=$(($money - $initial_bet))
    random_number=$(($RANDOM % 37))
    if [ ! "$money" -lt 0 ]; then
      # TODO Numeros pares
      if [ "$par_impar" == "par" ]; then
        if [ "$((random_number % 2))" -eq 0 ]; then
          if [ "$random_number" -eq 0 ]; then
            initial_bet=$(($initial_bet*2))
            jugadas_malas+="$random_number "
          else
            reward=$(($initial_bet*2))
            money=$(($money + $reward))
            initial_bet=$backup_initial_bet
            jugadas_malas=""
            if [ "$money" -ge "$mayor_dinero" ]; then
              mayor_dinero=$money
            fi
          fi
        else
          initial_bet=$(($initial_bet*2))
          jugadas_malas+="$random_number "
        fi
      else
        # TODO Numeros impares
        if [ "$((random_number % 2))" -eq 1 ]; then
          if [ "$random_number" -eq 0 ]; then
            initial_bet=$(($initial_bet*2))
            jugadas_malas+="$random_number "
          else
            reward=$(($initial_bet*2))
            money=$(($money + $reward))
            initial_bet=$backup_initial_bet
            jugadas_malas=""
            if [ "$money" -ge "$mayor_dinero" ]; then
              mayor_dinero=$money
            fi
          fi
        else
          initial_bet=$(($initial_bet*2))
          jugadas_malas+="$random_number "
        fi
      fi
    else
      #!Nos quedamos sin dinero
      echo -e "\n${redColour}[x]${endColour} ${grayColour}Te has quedado sin dinero${endColour} ${redColour}[x]${endColour}\n"
      echo -e "${yellowColour}[+]${endColour}${grayColour} Han habido un total de:${endColour}${blueColour} $(($play_counter-1))${endColour}${grayColour} jugadas${endColour}"
      echo -e "\n${yellowColour}[+]${endColour}${grayColour} Mayor cantidad de dinero alcanzado${endColour}${blueColour} $mayor_dinero$ ${endColour}"
      echo -e "\n${yellowColour}[+]${endColour}${grayColour} A continuacion se mostraran la cantidad de jugadas malas consecutivas que han salido:${endColour}\n"
      echo -e "${blueColour}[ $jugadas_malas]${endColour}"
      tput cnorm; exit 0
    fi

    let play_counter+=1
  done

  tput cnorm 
} 
#! Fin Martingala

# FIXME: Implementar la logica de Labouchere Inversa

# !Labouchere Inversa
function inverseLabouchere(){ 
  echo -e "\n${yellowColour}[+]${endColour}${grayColour} Tu dinero actual es:${endColour} ${blueColour}$money$ ${endColour}"
  echo -ne "${yellowColour}[+]${endColour}${grayColour} A que desea apostar continuamente (par/impar)?${endColour}${yellowColour} -->${endColour} " && read par_impar

  declare -a my_sequence=(1 2 3 4)

  echo -e "\n${yellowColour}[+]${endColour}${grayColour} Comenzaremos con  la secuencia ${endColour}${blueColour}[${my_sequence[@]}]${endColour}"

  bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))

  jugadas_totales=0
  jugadas_malas=""
  bet_to_renew=$(($money+50)) # Dinero que al alcanzarlo hara que renovemos nuestra secuencia a [1 2 3 4]
  mayor_dinero=$money
  tput civis 
  while true; do
    let jugadas_totales+=1
    money=$(($money - $bet))
    random_number=$(($RANDOM % 37))
    if [ ! "$money" -lt 0 ]; then

      # TODO El numero es par
      if [ "$par_impar" == "par" ]; then
        if [ "$(($random_number % 2))" -eq 0 ] && [ "$random_number" -ne 0 ]; then
          reward=$(($bet*2))
          jugadas_malas=""
          let money+=$reward
          if [ "$money" -ge "$mayor_dinero" ]; then
            mayor_dinero=$money
          fi 
          if [ $money -gt $bet_to_renew ]; then
            bet_to_renew=$(($bet_to_renew + 50))
            my_sequence=(1 2 3 4)
            bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
          else
            my_sequence+=($bet)
            my_sequence=(${my_sequence[@]})

            if [ "${#my_sequence[@]}" -ne 1 ] && [ "${#my_sequence[@]}" -ne 0 ]; then
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            elif [ "${#my_sequence[@]}" -eq 1 ]; then
              bet=${my_sequence[0]}
            else
              my_sequence=(1 2 3 4)
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            fi
          fi
        elif [ "$(($random_number % 2))" -eq 1 ] || [ "$random_number" -eq 0 ]; then
          jugadas_malas+="$random_number "
          if [ $money -lt $(($bet_to_renew-100)) ]; then 
            bet_to_renew=$(($bet_to_renew - 50))
            unset my_sequence[0]
            unset my_sequence[-1] 2>/dev/null

            my_sequence=(${my_sequence[@]})

            if [ "${#my_sequence[@]}" -ne 1 ] && [ "${#my_sequence[@]}" -ne 0 ]; then
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            elif [ "${#my_sequence[@]}" -eq 1 ]; then
              bet=${my_sequence[0]}
            else
              my_sequence=(1 2 3 4)
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            fi

          else
            unset my_sequence[0]
            unset my_sequence[-1] 2>/dev/null

            my_sequence=(${my_sequence[@]})

            if [ "${#my_sequence[@]}" -ne 1 ] && [ "${#my_sequence[@]}" -ne 0 ]; then
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            elif [ "${#my_sequence[@]}" -eq 1 ]; then
              bet=${my_sequence[0]}
            else
              my_sequence=(1 2 3 4)
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            fi
          fi
        fi 
      fi
      # TODO El numero es impar
      if [ "$par_impar" == "impar" ]; then
        if [ "$(($random_number % 2))" -eq 1 ] && [ "$random_number" -ne 0 ]; then
          reward=$(($bet*2))
          jugadas_malas=""
          let money+=$reward
          if [ "$money" -ge "$mayor_dinero" ]; then
            mayor_dinero=$money
          fi 
          if [ $money -gt $bet_to_renew ]; then
            bet_to_renew=$(($bet_to_renew + 50))
            my_sequence=(1 2 3 4)
            bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
          else
            my_sequence+=($bet)
            my_sequence=(${my_sequence[@]})

            if [ "${#my_sequence[@]}" -ne 1 ] && [ "${#my_sequence[@]}" -ne 0 ]; then
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            elif [ "${#my_sequence[@]}" -eq 1 ]; then
              bet=${my_sequence[0]}
            else
              my_sequence=(1 2 3 4)
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            fi
          fi
        elif [ "$(($random_number % 2))" -eq 0 ] || [ "$random_number" -eq 0 ]; then
          jugadas_malas+="$random_number "
          if [ $money -lt $(($bet_to_renew-100)) ]; then 
            bet_to_renew=$(($bet_to_renew - 50))
            unset my_sequence[0]
            unset my_sequence[-1] 2>/dev/null

            my_sequence=(${my_sequence[@]})

            if [ "${#my_sequence[@]}" -ne 1 ] && [ "${#my_sequence[@]}" -ne 0 ]; then
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            elif [ "${#my_sequence[@]}" -eq 1 ]; then
              bet=${my_sequence[0]}
            else
              my_sequence=(1 2 3 4)
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            fi

          else
            unset my_sequence[0]
            unset my_sequence[-1] 2>/dev/null

            my_sequence=(${my_sequence[@]})

            if [ "${#my_sequence[@]}" -ne 1 ] && [ "${#my_sequence[@]}" -ne 0 ]; then
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            elif [ "${#my_sequence[@]}" -eq 1 ]; then
              bet=${my_sequence[0]}
            else
              my_sequence=(1 2 3 4)
              bet=$((${my_sequence[0]} + ${my_sequence[-1]} ))
            fi
          fi
        fi 
      fi

    else
      # ! Nos quedamos sin dinero
      echo -e "\n${redColour}[x]${endColour} ${grayColour}Te has quedado sin dinero${endColour} ${redColour}[x]${endColour}\n"
      echo -e "${yellowColour}[+]${endColour}${grayColour} Han habido un total de:${endColour}${blueColour} $jugadas_totales${endColour}${grayColour} jugadas totales\n${endColour}"
      echo -e "${yellowColour}[+]${endColour}${grayColour} Mayor cantidad de dinero alcanzado:${endColour}${blueColour} $mayor_dinero$ ${endColour}\n"
      echo -e "${yellowColour}[+]${endColour}${grayColour} La cantidad de jugadas malas consecutivas fueron:${endColour} "
      echo -e "\n${blueColour}[ $jugadas_malas]${endColour}\n"
      tput cnorm; exit 1
    fi

  done
  tput cnorm  
}
#! Fin Labouchere Inversa

while getopts "m:t:h" arg; do
  case $arg in
    m) money=$OPTARG;;
    t) technique=$OPTARG;;
    h) helpPanel;;
  esac
done

if [ $money ] && [ $technique ]; then
  if [ "$technique" == "martingala" ]; then
    martingala
  elif [ "$technique" == "LabouchereInversa" ]; then
    inverseLabouchere
  else
    # ! La técnica no existe
    echo -e "\n${redColour}[!]${endColour}${grayColour}La tecnica${endColour}${blueColour} $technique${endColour}${grayColour} no existe${endColour}"
    helpPanel
  fi
else
  helpPanel
fi