function Change_Final_Time() {
        local yaml_file="$1"
        local new_final_time="$2"

        yq eval '.["Final Time"] = '"$new_final_time"'' -i "$yaml_file"

        if [ $? -eq 0 ]; then
                echo "Final Time has been updated"
        else
                echo "Failed to update"
        fi
}

function Run_Cases() {
        local yaml_file="$1"
        local first_time="$2"
        local last_time="$3"
        local thermal_yaml_file="thermal_linear_pyrolysis.yaml"

        for ((i=first_time; i<=last_time; i++)); do
                echo "Current Final Time: $i"
                Change_Final_Time "$yaml_file" $((i * 10))
                ./main input.yaml
                adv_term=$(yq eval '.materials[] | select(.name == "linear-tacot") | .["include advective energy balance term"]' "$thermal_yaml_file")
                echo "$adv_term"
                if [ "$adv_term" == "True" ]; then
                        mv OUTPUT/ "OUTPUT_FinalTime_$((i * 10))_advective"/
                else
                        mv OUTPUT/ "OUTPUT_FinalTime_$((i * 10))_no_adv"/
                fi
        done
}

Run_Cases "$1" "$2" "$3"
